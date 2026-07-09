from langchain_deepseek import ChatDeepSeek
from settings import DEEPSEEK_API_KEY
from langchain.agents import create_agent
from schemas.agent_schemas import QuestionResultSchema
from schemas.question_schemas import InterviewQuestionIn
import asyncio
import json

llm = ChatDeepSeek(
    model="deepseek-chat",
    api_key=DEEPSEEK_API_KEY,
    temperature=1
)

system_prompt = """
你是一位拥有 10+ 年一线研发经验的资深技术面试官（Tech Lead / Staff Engineer），深谙互联网大厂及独角兽公司的面试标准。你擅长通过行为面试法（Behavioral）、系统设计（System Design）和现场编码（Live Coding）相结合的方式，精准评估候选人的真实技术水平、工程素养及潜力。

请根据用户提供的参数，生成一套结构化的技术面试题。题目必须遵循以下严苛标准：

1. 实战导向：严禁出现纯概念背诵题（如“简述TCP三次握手”）。必须将考点融入真实业务场景（如高并发秒杀、数据一致性对账、性能瓶颈排查）。
2. 分层考察：题目需具备梯度，能从“基础实现”一路追问至“架构权衡”和“灾难恢复”。
3. 深度挖掘：答案（answer）不仅要给出标准解法，还需包含面试官视角的“考点解析”，明确指出候选人容易踩的坑（Pitfalls）。
4. 反模式规避：避免出脑筋急转弯或依赖特定编译器未定义行为的题目。

题目设计原则：
*   Code Quality：关注代码的鲁棒性、可读性及边界条件处理。
*   Trade-offs：强调技术方案的取舍（Time vs Space, Consistency vs Availability）。
*   Scalability：考察系统在流量激增下的扩展能力。
*   Debugging：考察线上故障的定位与解决思路。

输出要求：
请只返回符合以下结构的 JSON，不要输出 Markdown 或额外解释。确保 `points` 数组中包含“核心考察点”和“加分项”。

{
  "questions": [
    {
      "question": "具体的题目描述，包含背景约束和业务场景。",
      "points": ["考察点1：如时间复杂度优化", "考察点2：如分布式锁的使用"]
    }
  ]
}
"""

agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    response_format=QuestionResultSchema
)

async def generate_interview_questions(question_info: InterviewQuestionIn) -> QuestionResultSchema:
    content = f"用户面试的职位是：{question_info.job_title}，级别是：{question_info.seniority}，公司类型是：{question_info.company_type}，技术栈是：{question_info.tech_stack}，问题数量是：{question_info.question_count}，其他要求为：{question_info.other}"
    result = await agent.ainvoke({
        "messages": [{"role": "user", "content": content}]
    })
    # print(result)
    return result['structured_response']

# async def main():
#     name_info = NameIn(
#         surname="张",
#         gender="女",
#         length="两字"
#     )

#     names = await generate_names(name_info)
#     print(names)

# if __name__ == "__main__":
#     asyncio.run(main())
