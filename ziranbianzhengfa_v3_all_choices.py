import random
from typing import Dict, List, Optional

# ============================================================
# 自然辩证法刷题脚本：匹配题 + 选择题
# 说明：
# 1. MATCHING_DATA 保留你原来“观点—人物/答案”的练习方式，并补充了图片和历年回忆中的高频点。
# 2. CHOICE_QUESTIONS 是我把上传材料和图片中的选择题整理成的题库。
# 3. 有完整 A/B/C/D 选项的题，会按原选项出题；只有“题干—答案”的回忆题，会自动生成干扰项。
# ============================================================

MATCHING_DATA = {'实证主义': '孔德',
 '世界本源是由水构成的': '泰勒斯',
 '科学发展模式为“P-TT-EE-P”&证伪主义（否定后件式）': '波普尔',
 '知识就是力量': '弗朗西斯·培根',
 '机械唯物自然观的时间段': '16-18世纪',
 '地心主义/地心说': '托勒密',
 '世界本源是由无限构成的': '阿那克西曼德',
 '《科学：无尽的前沿》': '布什/拉什',
 '《自然辩证法》': '恩格斯',
 '“星云假说”': '康德',
 '“器官投影说” ：人和观点对应起来': '恩斯特·卡普',
 '《两种文化》(科学文化与人文文化)': 'C.P.斯诺',
 '具体分析“技术中心论”是错误的': '海德格尔',
 '《十七世纪英格兰的科学、技术与社会》开创科学社会学研究的新领域': '罗伯特.K.默顿',
 '《寂静的春天》': '卡逊',
 '《增长的极限》': '米杜斯',
 '国家创新体系': '弗里曼',
 '演绎-律则模型（DN模型）': '亨普尔',
 '（机械观）数原本论': '毕达哥拉斯',
 '古代原子论': '德谟克里特',
 '地动说': '阿里斯塔克',
 '位移运动说': '亚里士多德',
 '地质“渐变论”': '赖尔',
 '《单向度的人》': '马尔库塞',
 '机械唯物主义自然观诞生于哪个世纪？': '16-18世纪',
 '耗散结构理论': '伊里亚·普里戈金',
 '《科学史及其与哲学和宗教的关系》': '西耳·丹皮尔',
 '《第三次浪潮》是信息革命阶段': '托夫勒',
 '在《1844年经济学哲学手稿》中首次提出“劳动异化”的概念': '马克思',
 '逻辑实证主义': '维特根斯坦',
 '证伪主义': '波珀',
 '精致证伪主义': '拉卡托斯',
 '历史主义': '库恩',
 '《后工业社会》': '丹尼尔贝尔',
 '《知识社会》': '罗伯特E莱恩',
 '第一个提出发工资/提供经费支持': '法兰西皇家科学院',
 '第一个建立系和研究生院制度': '美国',
 '“种子说”': '阿那克萨戈拉',
 '“火本原说“': '赫拉克利特',
 '技术自主论代表': '雅克·埃吕尔',
 '范式概念/科学革命论/历史主义模式': '库恩',
 '科学研究纲领': '拉卡托斯',
 '科学社会学之父': '罗伯特·K·默顿',
 '《大地的伦理》': '利奥波德',
 '《增长的极限》报告机构': '罗马俱乐部',
 '演绎方法': '从一般到个别',
 '归纳方法': '从个别到一般',
 '科学从什么开始': '问题',
 '不属于顿悟的特征': '计划性',
 '第二次工业革命时间': '19世纪末到20世纪初',
 '“第三次浪潮”指的是': '信息革命',
 '《第三次浪潮》的作者': '托夫勒',
 '《科学，无止境的前沿》': '万·布什',
 '波普尔证伪主义的论证方式': '否定后件式',
 '清教文化影响最大的科学革命国家': '英国',
 '默顿科学共同体内部行为规范不包括': '权威主义',
 '辩证唯物主义科学基础不包括': '爱因斯坦的相对论'}

CHOICE_QUESTIONS = [{'question': '《自然辩证法》的作者是谁？',
  'options': {'A': '马克思', 'B': '黑格尔', 'C': '恩格斯', 'D': '康德'},
  'answer': 'C',
  'source': '选择题.docx/练习题'},
 {'question': '下列哪一个不是朴素唯物主义自然观的基本特征？',
  'options': {'A': '整体性和直观性', 'B': '思辨性和臆测性', 'C': '自发性和不彻底性', 'D': '夸张性和修辞性'},
  'answer': 'D',
  'source': '选择题.docx/练习题'},
 {'question': '下列哪个人是古代原子论的提出者？',
  'options': {'A': '苏格拉底', 'B': '亚里士多德', 'C': '德谟克利特', 'D': '毕达哥拉斯'},
  'answer': 'C',
  'source': '选择题.docx/练习题'},
 {'question': '下列哪一种自然观是马克思主义自然观的当代形态？',
  'options': {'A': '朴素唯物主义自然观', 'B': '机械唯物主义自然观', 'C': '系统自然观', 'D': '生态自然观'},
  'answer': 'D',
  'source': '选择题.docx/练习题',
  'note': '有资料认为系统自然观、生态自然观都属于当代形态；本题按上传选择题答案记D。'},
 {'question': '牛顿的自然观属于下列哪种？',
  'options': {'A': '朴素唯物主义自然观', 'B': '机械论自然观', 'C': '系统论自然观', 'D': '人工自然观'},
  'answer': 'B',
  'source': '选择题.docx/练习题'},
 {'question': '以下不属于马克思、恩格斯科学技术思想形成的科学技术基础的是？',
  'options': {'A': '能量守恒与转化定律', 'B': '元素周期律', 'C': '细胞学说', 'D': '生物进化论'},
  'answer': 'B',
  'source': '选择题.docx/练习题'},
 {'question': '以下不属于西方科学哲学代表性流派的是？',
  'options': {'A': '逻辑实证主义', 'B': '历史主义', 'C': '机会主义', 'D': '证伪主义'},
  'answer': 'C',
  'source': '选择题.docx/2025秋回忆'},
 {'question': '下列关于科学本质特征的理解错误的是？',
  'options': {'A': '科学是理论化、系统化的知识体系', 'B': '科学是产生知识体系的认识活动', 'C': '科学是一种文化现象', 'D': '科学是人的本质力量的对象化'},
  'answer': 'D',
  'source': '选择题.docx/练习题'},
 {'question': '提出“器官投影说”的哲学家是？',
  'options': {'A': '卡普', 'B': '芒福德', 'C': '海德格尔', 'D': '马尔库塞'},
  'answer': 'A',
  'source': '选择题.docx/2025秋回忆'},
 {'question': '以下不属于科学知识结构的是？',
  'options': {'A': '科学事实', 'B': '科学假说', 'C': '科学实验', 'D': '科学理论'},
  'answer': 'C',
  'source': '选择题.docx/练习题'},
 {'question': '马克思科学技术方法论的核心是？',
  'options': {'A': '公理化方法', 'B': '分析与归纳', 'C': '批判性思维', 'D': '辩证思维与系统思维'},
  'answer': 'D',
  'source': '选择题.docx/练习题'},
 {'question': '下面哪个不是技术预测的基本类型？',
  'options': {'A': '顶层设计预测', 'B': '类比性预测', 'C': '归纳性预测', 'D': '演绎性预测'},
  'answer': 'A',
  'source': '选择题.docx/练习题'},
 {'question': '著名科学哲学家波普尔强调，科学从什么开始？',
  'options': {'A': '观察', 'B': '实验', 'C': '数据', 'D': '问题'},
  'answer': 'D',
  'source': '选择题.docx/历年回忆'},
 {'question': '归纳是一种什么方法？',
  'options': {'A': '从一般性前提推出个别性结论的认识方法',
              'B': '从个别到一般的推理方法，寻求事物普遍特征的认识方法',
              'C': '把对象分解为各个部分分别研究考察的方法',
              'D': '以批判性思考方式质疑和评估思考过程与结果的方法'},
  'answer': 'B',
  'source': '选择题.docx/历年回忆'},
 {'question': '下面不属于非逻辑思维的是？',
  'options': {'A': '分析', 'B': '直觉', 'C': '灵感', 'D': '顿悟'},
  'answer': 'A',
  'source': '选择题.docx/练习题'},
 {'question': '以下哪位学者提出了“两种文化”观念？',
  'options': {'A': '罗伯特·K·默顿', 'B': 'C.P.斯诺', 'C': '海德格尔', 'D': '哈贝马斯'},
  'answer': 'B',
  'source': '选择题.docx/练习题'},
 {'question': '技术共同体的最高目标是？',
  'options': {'A': '人类、社会、经济和谐发展', 'B': '人类、社会、自然和谐发展', 'C': '人类、自然、经济和谐发展', 'D': '社会、自然、经济和谐发展'},
  'answer': 'B',
  'source': '选择题.docx/练习题'},
 {'question': '技术文化的核心是？',
  'options': {'A': '文化至上原则', 'B': '技术理性', 'C': '技术、文化合理协调', 'D': '技术至上原则'},
  'answer': 'B',
  'source': '选择题.docx/练习题'},
 {'question': '技术中心论/技术中性论是错误的，对这一观点展开具体分析的学者是？',
  'options': {'A': '罗伯特·K·默顿', 'B': 'C.P.斯诺', 'C': '海德格尔', 'D': '哈贝马斯'},
  'answer': 'C',
  'source': '选择题.docx/练习题'},
 {'question': '以下哪项不属于科学的社会建制化表现形式？',
  'options': {'A': '十七世纪英国皇家学会和法国皇家学会成立', 'B': '亚里士多德逍遥学派', 'C': '德国大学实验室制度', 'D': '美国大学系和研究生院制度'},
  'answer': 'B',
  'source': '选择题.docx/练习题'},
 {'question': '法兰克福学派主要观点不包括？',
  'options': {'A': '现代科学技术把人变成商品的奴隶、消费的奴隶', 'B': '现代科学技术具有意识形态功能', 'C': '现代科学技术成为独裁手段', 'D': '现代科学技术价值中立'},
  'answer': 'D',
  'source': '选择题.docx/2025秋回忆'},
 {'question': '科学技术的社会建制要素不包括？',
  'options': {'A': '组织机构', 'B': '社会体制', 'C': '合作机构/合作机制', 'D': '行为规范'},
  'answer': 'C',
  'source': '选择题.docx/2025秋回忆'},
 {'question': '《十七世纪英格兰的科学、技术与社会》开创科学社会学研究新领域，该论著出自谁？',
  'options': {'A': '罗伯特·K·默顿', 'B': 'C.P.斯诺', 'C': '海德格尔', 'D': '哈贝马斯'},
  'answer': 'A',
  'source': '选择题.docx/练习题'},
 {'question': '清教文化对哪个国家历史上的科学革命有巨大影响？',
  'options': {'A': '意大利', 'B': '法国', 'C': '英国', 'D': '德国'},
  'answer': 'C',
  'source': '2025秋真题回忆图'},
 {'question': '默顿的科学共同体内部行为规范不包括？',
  'options': {'A': '普遍主义', 'B': '公有主义', 'C': '权威主义', 'D': '无私利主义'},
  'answer': 'C',
  'source': '2025秋真题回忆图'},
 {'question': '辩证唯物主义的科学基础不包括？',
  'options': {'A': '康德的星云假说', 'B': '维勒的人工合成尿素', 'C': '麦克斯韦的电磁场理论', 'D': '爱因斯坦的相对论'},
  'answer': 'D',
  'source': '2025秋真题回忆图'},
 {'question': '《第三次浪潮》的作者是？', 'answer': '托夫勒', 'source': '2025秋真题回忆图/原代码'},
 {'question': '《耗散论》或耗散结构理论是谁提出的？', 'answer': '普利高津（普里戈金）', 'source': '2025秋真题回忆图/历年回忆'},
 {'question': '卡逊是下列哪本书的作者？',
  'options': {'A': '《寂静的春天》', 'B': '《增长的极限》', 'C': '《科学革命的结构》', 'D': '《科学的社会功能》'},
  'answer': 'A',
  'source': '2021/2023/2024/2025回忆'},
 {'question': '实证主义是下列哪位科学家/思想家提出的？',
  'options': {'A': '库恩', 'B': '波普尔', 'C': '石里克', 'D': '孔德'},
  'answer': 'D',
  'source': '2021/2023回忆'},
 {'question': '“知识就是力量”是哪位思想家提出来的？',
  'options': {'A': '罗吉尔·培根', 'B': '弗朗西斯·培根', 'C': '阿奎那', 'D': '伽利略'},
  'answer': 'B',
  'source': '2021/2023回忆'},
 {'question': '《科学，无止境的前沿》是哪位科学家的作品？',
  'options': {'A': '万·布什', 'B': '爱因斯坦', 'C': '库恩', 'D': '贝尔纳'},
  'answer': 'A',
  'source': '2021/2023回忆'},
{'question': '下列哪个机构率先给科学家提供薪水？',
 'options': {'A': '英国皇家学会', 'B': '法国科学院', 'C': '瑞典科学院', 'D': '美国科学院'},
  'answer': 'B',
  'source': '2021回忆',
  'note': "按当前确认口径：正确答案为法国科学院。"},
 {'question': '“耗散结构理论”是由哪位学者提出的？',
  'options': {'A': '普利高津', 'B': '哈肯', 'C': '托姆', 'D': '牛顿'},
  'answer': 'A',
  'source': '2021/2024/2025回忆'},
 {'question': '波普尔“证伪主义”的论证方式是？',
  'options': {'A': '否定前件式', 'B': '否定后件式', 'C': '肯定前件式', 'D': '肯定后件式'},
  'answer': 'B',
  'source': '2021/2023/2024回忆'},
 {'question': '“世界的本源是由无限构成的”是由哪位哲学家首先提出来的？',
  'options': {'A': '苏格拉底', 'B': '毕达哥拉斯', 'C': '泰勒斯', 'D': '阿那克西曼德'},
  'answer': 'D',
  'source': '2021回忆/2025照片'},
 {'question': '《科学史及其与哲学和宗教的关系》的作者是？', 'answer': '丹皮尔', 'source': '2021回忆/2025照片'},
 {'question': '“第三次浪潮”指的是？', 'answer': '信息革命', 'source': '2021回忆/2025照片'},
 {'question': '演绎方法的基本方向是？', 'answer': '从一般到个别', 'source': '2024.12回忆'},
 {'question': '科学研究纲领是谁提出的？', 'answer': '拉卡托斯', 'source': '2023/2024/2025回忆'},
 {'question': '范式概念是谁提出的？', 'answer': '库恩', 'source': '2023/2024回忆'},
 {'question': '哪一项不属于顿悟？', 'answer': '计划性', 'source': '2023/2024/2025照片'},
 {'question': '《大地的伦理》作者是谁？', 'answer': '利奥波德', 'source': '2024/2025照片'},
 {'question': '创新理论是谁最先提出的？', 'answer': '熊彼特', 'source': '2023/2024/2025照片'},
 {'question': '提出“水是万物本原/本源”的是谁？', 'answer': '泰勒斯', 'source': '2023/2024/2025照片'},
 {'question': '《单向度的人》最可能对应哪个时期？', 'answer': '工业革命', 'source': '2024.5回忆/2025照片'},
 {'question': '科学社会学之父是谁？', 'answer': '罗伯特·K·默顿', 'source': '2024.5回忆/2025照片'},
 {'question': '科学革命论、范式、历史主义模式主要对应哪位学者？', 'answer': '库恩', 'source': '2023.5回忆'},
 {'question': '《增长的极限》由哪个机构报告/提出？', 'answer': '罗马俱乐部', 'source': '2024.5回忆/2025照片'},
 {'question': '耗散结构不包含以下哪个要素？',
  'options': {'A': '非线性相互作用', 'B': '非平衡态', 'C': '因果关系', 'D': '开放系统'},
  'answer': 'C',
  'source': '2024.5回忆',
  'note': "原回忆写'不保证正确'，这里按上传回忆中笔者选择整理。"},
 {'question': '下面哪种品质不适合把握机遇？',
  'options': {'A': '敏锐的洞察力', 'B': '科学的想象力', 'C': '较强的判断力', 'D': '执着'},
  'answer': 'D',
  'source': '2024.5回忆',
  'note': "原回忆注明'不保证正确'，C项为根据题意补全。"},
 {'question': '地心说由谁提出？', 'answer': '托勒密', 'source': '2023.5考后回忆/原代码'},
 {'question': '第二次工业革命时间大致是？', 'answer': '19世纪末到20世纪初', 'source': '2023/2025照片'},
 {'question': '技术自主论的代表人物是谁？', 'answer': '雅克·埃吕尔', 'source': '2025照片/原代码'},
 {'question': '机械唯物主义自然观大致诞生于哪个世纪？', 'answer': '16—18世纪', 'source': '原代码/常考点'}]


def get_correct_text(question: Dict) -> str:
    """返回题目的正确答案文本。"""
    options = question.get("options")
    answer = question.get("answer")
    if options and answer in options:
        return options[answer]
    return str(answer)


def build_answer_pool() -> List[str]:
    """用于给只有答案、没有固定选项的回忆题生成干扰项。"""
    pool = set(MATCHING_DATA.values())
    for q in CHOICE_QUESTIONS:
        pool.add(get_correct_text(q))
        for v in q.get("options", {}).values():
            pool.add(v)
    return sorted(pool)


def generate_options(correct: str, answer_pool: List[str], n: int = 4) -> Dict[str, str]:
    """给无选项题生成 A/B/C/D。"""
    distractors = [x for x in answer_pool if x != correct]
    k = max(0, min(n - 1, len(distractors)))
    options = random.sample(distractors, k) + [correct]
    random.shuffle(options)
    return {chr(65 + i): opt for i, opt in enumerate(options)}


def normalize_choice(s: str) -> str:
    return s.strip().upper().replace("。", "").replace(".", "")


def ask_choice_questions(questions: Optional[List[Dict]] = None, shuffle: bool = True, limit: Optional[int] = None) -> None:
    """选择题练习。"""
    if questions is None:
        questions = CHOICE_QUESTIONS.copy()
    else:
        questions = questions.copy()

    if shuffle:
        random.shuffle(questions)
    if limit is not None:
        questions = questions[:limit]

    answer_pool = build_answer_pool()
    score = 0
    wrong_answers = []

    for i, q in enumerate(questions, 1):
        correct_text = get_correct_text(q)
        fixed_options = q.get("options")
        if fixed_options:
            options = fixed_options
            correct_letter = q.get("answer")
        else:
            options = generate_options(correct_text, answer_pool)
            correct_letter = next(k for k, v in options.items() if v == correct_text)

        print(f"\n选择题 {i}/{len(questions)}：{q['question']}")
        if q.get("source"):
            print(f"来源：{q['source']}")
        for letter in sorted(options):
            print(f"{letter}. {options[letter]}")

        user_choice = normalize_choice(input("请输入选项编号，或输入 q 退出："))
        if user_choice == "Q":
            break

        # 支持输入字母，也支持直接输入答案文字。
        is_right = False
        if user_choice in options:
            is_right = options[user_choice] == correct_text
        else:
            is_right = user_choice == normalize_choice(correct_text)

        if is_right:
            print("回答正确！")
            score += 1
        else:
            print(f"回答错误。正确答案：{correct_letter}. {correct_text}")
            wrong_answers.append({
                "question": q["question"],
                "your_choice": user_choice,
                "correct": f"{correct_letter}. {correct_text}",
                "source": q.get("source", "")
            })

        if q.get("note"):
            print(f"提示：{q['note']}")

    print("\n====================")
    print(f"本次得分：{score}/{len(questions)}")
    if wrong_answers:
        print("\n错题回顾：")
        for item in wrong_answers:
            print(f"- {item['question']}")
            print(f"  你的答案：{item['your_choice']}；正确答案：{item['correct']}；来源：{item['source']}")


def ask_matching_questions(data: Optional[Dict[str, str]] = None, shuffle: bool = True, limit: Optional[int] = None) -> None:
    """保留你原来的“观点—人物/答案”匹配练习。"""
    if data is None:
        data = MATCHING_DATA

    views = list(data.keys())
    if shuffle:
        random.shuffle(views)
    if limit is not None:
        views = views[:limit]

    all_answers = sorted(set(data.values()))
    score = 0
    wrong_answers = []

    for i, view in enumerate(views, 1):
        correct = data[view]
        distractors = [a for a in all_answers if a != correct]
        options = random.sample(distractors, min(3, len(distractors))) + [correct]
        random.shuffle(options)
        options_dict = {chr(65 + j): person for j, person in enumerate(options)}

        print(f"\n匹配题 {i}/{len(views)}：{view}")
        for option in sorted(options_dict):
            print(f"{option}. {options_dict[option]}")

        user_choice = normalize_choice(input("请输入选项编号，或输入 q 退出："))
        if user_choice == "Q":
            break

        if options_dict.get(user_choice) == correct:
            print("回答正确！")
            score += 1
        else:
            print(f"回答错误。正确答案：{correct}")
            wrong_answers.append((view, user_choice, correct))

    print("\n====================")
    print(f"本次得分：{score}/{len(views)}")
    if wrong_answers:
        print("\n错题回顾：")
        for view, choice, correct in wrong_answers:
            print(f"- {view}；你的选择：{choice}；正确答案：{correct}")


def main() -> None:
    print("自然辩证法刷题程序")
    print(f"选择题题库：{len(CHOICE_QUESTIONS)} 道")
    print(f"匹配题题库：{len(MATCHING_DATA)} 条")
    print("1. 只练选择题")
    print("2. 只练观点—人物/答案匹配题")
    print("3. 选择题 + 匹配题都练")

    mode = input("请选择模式（默认1）：").strip() or "1"
    limit_text = input("本次练几题？直接回车表示全部：").strip()
    limit = int(limit_text) if limit_text.isdigit() else None

    if mode == "2":
        ask_matching_questions(limit=limit)
    elif mode == "3":
        ask_choice_questions(limit=limit)
        ask_matching_questions(limit=limit)
    else:
        ask_choice_questions(limit=limit)


if __name__ == "__main__":
    main()
