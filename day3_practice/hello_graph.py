# hello_graph.py (작성 시작)
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    user_input: str
    response: str


def respond(state: State) -> dict:
    user = state["user_input"]                            # 1) State에서 읽고
    return {"response": f"입력하신 내용은 '{user}' 입니다."}  # 2) 갱신분만 반환


# 노드는 그냥 함수이므로 그래프 없이도 직접 호출해 볼 수 있습니다
# print(respond({"user_input": "테스트", "response": ""}))

builder = StateGraph(State)              # State 스키마를 알려주며 빌더 생성
builder.add_node("respond", respond)     # (노드 이름, 함수)

builder.add_edge(START, "respond")       # 시작에서 respond로
builder.add_edge("respond", END)         # respond에서 끝으로

graph = builder.compile()    # 그래프를 실행 가능한 객체로 변환

result = graph.invoke({"user_input": "안녕하세요"})
print(result)

# 구조 시각화: PNG 저장이 안 되는 환경도 있으므로 try/except로 감쌉니다
try:
    graph.get_graph().draw_mermaid_png(output_file_path="hello_graph.png")
    print("hello_graph.png 저장 완료")
except Exception as e:
    print("PNG 저장은 건너뜁니다:", e)
    print(graph.get_graph().draw_mermaid())   # 텍스트 출력으로 대체