# react_agent_prebuilt.py - create_react_agent로 같은 그래프 만들기
# 도구, 프롬프트, LLM은 react_agent.py의 것을 그대로 재사용하고
# (2/3) 그래프 조립 부분만 create_react_agent 한 줄로 바꿉니다.
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

from react_agent import llm, tools, SYSTEM_PROMPT, print_message

# [StateGraph + agent 노드 + should_continue + ToolNode + 엣지 3개] -> create_react_agent
graph = create_react_agent(
    model=llm,             # bind_tools(tools)는 내부에서 자동으로 해 줍니다
    tools=tools,           # 내부에서 ToolNode(tools)로 감싸 "tools" 노드가 됩니다
    prompt=SYSTEM_PROMPT,  # 매 호출마다 messages 앞에 SystemMessage로 붙습니다
)
# 기본 State는 messages: Annotated[list, add_messages] 를 가진 AgentState입니다.

try:
    graph.get_graph().draw_mermaid_png(output_file_path="react_agent_prebuilt.png")
    print("react_agent_prebuilt.png 저장 완료")
except Exception as e:
    print("PNG 저장은 건너뜁니다:", e)
    print(graph.get_graph().draw_mermaid())


def run_and_trace_stream(question: str):
    print(f"\n{'=' * 60}\n질문: {question}\n{'=' * 60}")
    printed = 0
    for state in graph.stream({"messages": [HumanMessage(content=question)]}, stream_mode="values"):
        for m in state["messages"][printed:]:
            print_message(m)
        printed = len(state["messages"])


if __name__ == "__main__":
    run_and_trace_stream("어떤 일을 도와줄 수 있는지 한 문장으로 소개해줘.")
    run_and_trace_stream("박도윤 님 이메일을 알려주고, '연차 이월 기준이 궁금해요' 문의의 담당 부서도 분류해줘.")
