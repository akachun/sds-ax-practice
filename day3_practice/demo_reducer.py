# demo_reducer.py - add_messages 가 id 로 합친다는 것을 눈으로 보기
from langchain_core.messages import AIMessage
from langgraph.graph.message import add_messages

기존 = [AIMessage(content="첫 답변", id="m1")]

print("=== 새 id 로 넣으면 ===")
print([m.content for m in add_messages(기존, [AIMessage(content="두 번째", id="m2")])])

print("\n=== 같은 id 로 넣으면 ===")
print([m.content for m in add_messages(기존, [AIMessage(content="고친 답변", id="m1")])])