
import re

from typing import TypedDict, Annotated

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from services.conversationMemoryService import (
    CreateConversationCheckpointer,
    GetConversationConfig
)

from services.ragService import AnswerQuestion

from services.intentClassifierService import ClassifyIntent

from services.ticketService import (
    FindOrCreateSupportTicket,
    GetLatestNotificationAttempt
)

from services.webhookNotificationService import NotifySupportWebhook


class SupportState(TypedDict, total=False):
    question: str
    messages: Annotated[list, add_messages]
    route: str
    answer: str
    sources: list
    status: str
    intent: str
    thread_id: str
    ticket_id: str | None
    notification_status: str



def RouteRequest(state: SupportState):

    question = state["question"].strip()

    messages = state.get("messages", [])

    history = []

    # Exclude the current customer message,
    # which is already supplied separately.
    for message in messages[:-1]:

        if isinstance(message, HumanMessage):
            role = "Customer"

        elif isinstance(message, AIMessage):
            role = "Assistant"

        else:
            continue

        if isinstance(message.content, str):
            history.append(
                f"{role}: {message.content}"
            )

    intent = ClassifyIntent(
        question,
        history=history
    )

    if intent in [
        "policy_inquiry",
        "product_inquiry",
        "technical_support"
    ]:
        route = "rag"

    elif intent in [
        "order_account",
        "human_support"
    ]:
        route = "human"

    else:
        route = "fallback"

    return {
        "intent": intent,
        "route": route
    }


def BuildContextualQuestion(state: SupportState):

    question = state["question"].strip()

    messages = state.get("messages", [])

    previous_questions = [
        message.content
        for message in messages[:-1]
        if isinstance(message, HumanMessage)
        and isinstance(message.content, str)
    ]

    if not previous_questions:
        return question

    follow_up_patterns = [
        r"^what if\b",
        r"^what about\b",
        r"^how about\b",
        r"^and (?:what|if|can|does)\b",
        r"^does that\b",
        r"^is that\b",
        r"^what happens if\b"
    ]

    is_follow_up = any(
        re.search(pattern, question.lower())
        for pattern in follow_up_patterns
    )

    if is_follow_up:
        return (
            f"Previous customer question: "
            f"{previous_questions[-1]}\n"
            f"Follow-up question: {question}"
        )

    return question


def RAGAnswer(state: SupportState):

    contextual_question = BuildContextualQuestion(state)

    result = AnswerQuestion(contextual_question)

    answer = result["answer"]
    status = result["status"]

    unsafe_patterns = [
        r"\b(?:i|we)\s+(?:can|will|'ll|’ll)\s+"
        r"(?:look\s+it\s+up|retrieve|check\s+your\s+order|"
        r"access\s+your\s+account|track\s+your\s+order|"
        r"process\s+your\s+refund)\b"
    ]

    if any(
        re.search(pattern, answer.lower())
        for pattern in unsafe_patterns
    ):
        return {
            "answer": (
                "I can explain our published policies, "
                "but I cannot access private order or "
                "account information in this chat. "
                "Please contact our official support "
                "channel for an authorized lookup."
            ),
            "sources": [],
            "status": "needs_review"
        }

    return {
        "answer": answer,
        "sources": result["sources"],
        "status": status
    }





def HumanReview(state: SupportState):

    result = FindOrCreateSupportTicket(
        thread_id=state["thread_id"],
        customer_message=state["question"],
        intent=state["intent"]
    )

    ticket = result["ticket"]
    created = result["created"]

    ticket_id = ticket["ticket_id"]

    if created:

        try:
            notification = NotifySupportWebhook(
                ticket_id
            )

            delivery_status = notification[
                "delivery_status"
            ]

        except Exception:
            delivery_status = "failed"

        message = (
            "Your request has been recorded for "
            "human support review."
        )

    else:

        latest = GetLatestNotificationAttempt(
            ticket_id
        )

        delivery_status = (
            latest["delivery_status"]
            if latest
            else "not_attempted"
        )

        message = (
            "You already have an active support "
            "ticket for this request. "
            "I've reused the existing ticket."
        )

    return {
        "answer": (
            f"{message}\n\n"
            f"Support Ticket: {ticket_id}\n"
            f"Status: {ticket['status']}\n\n"
            "A support representative will need "
            "to review your request. "
            "No response time has been confirmed."
        ),
        "ticket_id": ticket_id,
        "notification_status": delivery_status,
        "sources": [],
        "status": "needs_review"
    }


def SafeFallback(state: SupportState):

    return {
        "answer": (
            "I don't have enough verified information "
            "to answer that request. A support "
            "representative can review it."
        ),
        "sources": [],
        "status": "needs_review",
        "ticket_id": None,
        "notification_status": "not_attempted"
    }



def RecordTurn(state: SupportState):

    return {
        "messages": [
            AIMessage(content=state["answer"])
        ]
    }


def ChooseRoute(state: SupportState):
    return state["route"]


def CheckAnswer(state: SupportState):

    if state["status"] == "needs_review":
        return "fallback"

    return "done"









def BuildCustomerSupportAgent():

    graph = StateGraph(SupportState)

    graph.add_node("RouteRequest", RouteRequest)
    graph.add_node("RAGAnswer", RAGAnswer)
    graph.add_node("HumanReview", HumanReview)
    graph.add_node("SafeFallback", SafeFallback)
    graph.add_node("RecordTurn", RecordTurn)

    graph.add_edge(START, "RouteRequest")

    graph.add_conditional_edges(
        "RouteRequest",
        ChooseRoute,
        {
            "rag": "RAGAnswer",
            "human": "HumanReview",
            "fallback": "SafeFallback"
        }
    )

    graph.add_conditional_edges(
        "RAGAnswer",
        CheckAnswer,
        {
            "done": "RecordTurn",
            "fallback": "SafeFallback"
        }
    )

    graph.add_edge("HumanReview", "RecordTurn")
    graph.add_edge("SafeFallback", "RecordTurn")
    graph.add_edge("RecordTurn", END)

    checkpointer = CreateConversationCheckpointer()

    return graph.compile(
        checkpointer=checkpointer
    )

customerSupportAgent = BuildCustomerSupportAgent()



def RunCustomerSupportAgent(
    question,
    thread_id="default"
):

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question cannot be empty")

    if not isinstance(thread_id, str) or not thread_id.strip():
        raise ValueError("Thread ID cannot be empty")

    config = GetConversationConfig(thread_id)

    result = customerSupportAgent.invoke(
        {
            "question": question,
            "thread_id": thread_id,
            "ticket_id": None,
            "notification_status": "not_attempted",
            "messages": [
                HumanMessage(content=question)
            ]
        },
        config=config
    )

    return result
