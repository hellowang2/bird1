import tkinter as tk
from tkinter import ttk
from itertools import product

#經驗之談與猜測

# 定義顏色基因型和表現型對應
# 性聯遺傳的基因
# 雄性為 ZZ，雌性為 ZW
# 基因位於 Z 染色體上的有 R (紅頭), b (黑頭), r^y (黃頭), Y (黃色)

# 背部和胸部基因為常染色體
# G (綠背), b (藍背), Y (黃色)
# P (紫胸), w (白胸)

# 定義基因型到表現型的映射
def determine_head_color(sex, father_head, mother_head):
    """
    根據性別和父母的頭部基因，確定子代的頭部表現型
    """
    head_phenotypes = []
    
    if sex == 'male':
        # 雄性有兩個 Z 染色體，一個來自父親，一個來自母親
        possible_father_alleles = father_head
        possible_mother_alleles = mother_head
        for fa in possible_father_alleles:
            for ma in possible_mother_alleles:
                genotype = ''.join(sorted([fa, ma]))
                phenotype = interpret_head_genotype(genotype)
                head_phenotypes.append(phenotype)
    else:
        # 雌性有一個 Z 染色體來自父親，一個 W 染色體來自母親
        possible_father_alleles = father_head
        for fa in possible_father_alleles:
            genotype = fa  # 只有一個 Z 染色體基因
            phenotype = interpret_head_genotype_female(genotype)
            head_phenotypes.append(phenotype)
    
    return set(head_phenotypes)

def interpret_head_genotype(genotype):
    """
    根據雄性的頭部基因型確定表現型
    基因優勢: R > r^y > b
    藍背會壓制紅頭和黃頭，導致鮭魚色
    """
    if 'R' in genotype:
        if 'r^y' in genotype:
            return "橘頭"
        else:
            return "紅頭"
    elif 'r^y' in genotype:
        return "橘頭"
    elif genotype == 'bb':
        return "黑頭"
    else:
        return "未知頭部顏色"

def interpret_head_genotype_female(genotype):
    """
    根據雌性的頭部基因型確定表現型
    基因優勢: R > r^y > b
    """
    if genotype == 'R':
        return "紅頭"
    elif genotype == 'r^y':
        return "橘頭"
    elif genotype == 'b':
        return "黑頭"
    else:
        return "未知頭部顏色"

def determine_back_color(parent1_back, parent2_back):
    """
    根據父母的背部基因，確定子代的背部表現型
    基因優勢: G > Y > b
    """
    back_phenotypes = []
    for b1, b2 in product(parent1_back, parent2_back):
        genotype = ''.join(sorted([b1, b2]))
        phenotype = interpret_back_genotype(genotype)
        back_phenotypes.append(phenotype)
    return set(back_phenotypes)

def interpret_back_genotype(genotype):
    if 'G' in genotype:
        if 'Y' in genotype:
            return "黃背"
        else:
            return "綠背"
    elif 'Y' in genotype:
        return "黃背"
    elif genotype == 'bb':
        return "藍背"
    else:
        return "藍背"

def determine_chest_color(parent1_chest, parent2_chest):
    """
    根據父母的胸部基因，確定子代的胸部表現型
    基因優勢: P > w
    """
    chest_phenotypes = []
    for c1, c2 in product(parent1_chest, parent2_chest):
        genotype = ''.join(sorted([c1, c2]))
        phenotype = interpret_chest_genotype(genotype)
        chest_phenotypes.append(phenotype)
    return set(chest_phenotypes)

def interpret_chest_genotype(genotype):
    if 'P' in genotype:
        return "紫胸"
    elif genotype == 'ww':
        return "白胸"
    else:
        return "紫胸"#淡

def apply_gene_interactions(sex, head, back):
    """
    根據背部基因對頭部基因的影響，調整頭部表現型
    """
    if '藍背' in back:
        if head in ["紅頭", "橘頭"]:
            return "鮭魚色"  # 藍背壓制紅頭和橘頭
    if '黃色背部' in back:
        if head == "黑頭":
            return "黃頭"  # 黃色背部壓制黑頭
    return head

def calculate_offspring(parent1, parent2):
    offspring_results = []

    # 父母的基因型
    # parent1: 父親，ZZ
    # parent2: 母親，ZW

    # 分離父母的基因
    father_head = parent1['head']
    father_back = parent1['back']
    father_chest = parent1['chest']

    mother_head = parent2['head']
    mother_back = parent2['back']
    mother_chest = parent2['chest']

    # 產生子代的性別
    sexes = ['male', 'female']

    for sex in sexes:
        if sex == 'male':
            # 雄性子代，從父親和母親各獲得一個 Z 染色體基因
            child_head = determine_head_color(sex, father_head, mother_head)
        else:
            # 雌性子代，從父親獲得一個 Z 染色體基因，母親提供 W（無頭部基因）
            child_head = determine_head_color(sex, father_head, mother_head)

        # 背部基因
        child_back = determine_back_color(father_back, mother_back)

        # 胸部基因
        child_chest = determine_chest_color(father_chest, mother_chest)

        # 應用基因之間的相互作用
        final_heads = set()
        for h in child_head:
            adjusted_head = apply_gene_interactions(sex, h, child_back)
            final_heads.add(adjusted_head)

        # 應用背部基因對頭部基因的最終調整
        for h in final_heads:
            for b in child_back:
                for c in child_chest:
                    offspring_results.append({
                        'sex': sex,
                        'head': h,
                        'back': b,
                        'chest': c
                    })

    # 移除重複的結果
    unique_offspring = []
    seen = set()
    for bird in offspring_results:
        key = (bird['sex'], bird['head'], bird['back'], bird['chest'])
        if key not in seen:
            seen.add(key)
            unique_offspring.append(bird)

    return unique_offspring

# GUI 建立
def create_gui():
    def calculate():
        male = {
            'head': male_head_var.get().split('/'),
            'back': male_back_var.get().split('/'),
            'chest': male_chest_var.get().split('/')
        }
        female = {
            'head': female_head_var.get().split('/'),
            'back': female_back_var.get().split('/'),
            'chest': female_chest_var.get().split('/')
        }

        offspring = calculate_offspring(male, female)

        result_text.delete(1.0, tk.END)
        for bird in offspring:
            result_text.insert(tk.END, f"性別：{bird['sex']}，子代顏色：頭部 - {bird['head']}，背部 - {bird['back']}，胸部 - {bird['chest']}\n")

    # 建立主視窗
    root = tk.Tk()
    root.title("七彩文鳥基因計算器")

    # 公鳥和母鳥選項
    ttk.Label(root, text="父鳥基因型：").grid(row=0, column=0, padx=10, pady=5, sticky='w')
    male_frame = ttk.LabelFrame(root, text="父鳥 (雄性)")
    male_frame.grid(row=0, column=1, padx=10, pady=5)

    # 父鳥頭部基因
    ttk.Label(male_frame, text="頭部基因 (ZZ):").grid(row=0, column=0, sticky='w')
    male_head_var = tk.StringVar()
    male_head_combo = ttk.Combobox(male_frame, textvariable=male_head_var, values=[
        "R/R", "R/r", "r/r", "Ry/Ry", "Ry/r", "Ry/b", "b/b"
    ], state="readonly")
    male_head_combo.grid(row=0, column=1, padx=5, pady=2)
    male_head_combo.current(0)

    # 父鳥背部基因
    ttk.Label(male_frame, text="背部基因 (常染色體):").grid(row=1, column=0, sticky='w')
    male_back_var = tk.StringVar()
    male_back_combo = ttk.Combobox(male_frame, textvariable=male_back_var, values=[
        "G/G", "G/b", "G/Y", "b/b", "Y/Y"
    ], state="readonly")
    male_back_combo.grid(row=1, column=1, padx=5, pady=2)
    male_back_combo.current(0)

    # 父鳥胸部基因
    ttk.Label(male_frame, text="胸部基因 (常染色體):").grid(row=2, column=0, sticky='w')
    male_chest_var = tk.StringVar()
    male_chest_combo = ttk.Combobox(male_frame, textvariable=male_chest_var, values=[
        "P/P", "P/w", "w/w"
    ], state="readonly")
    male_chest_combo.grid(row=2, column=1, padx=5, pady=2)
    male_chest_combo.current(0)

    ttk.Label(root, text="母鳥基因型：").grid(row=1, column=0, padx=10, pady=5, sticky='w')
    female_frame = ttk.LabelFrame(root, text="母鳥 (雌性)")
    female_frame.grid(row=1, column=1, padx=10, pady=5)

    # 母鳥頭部基因
    ttk.Label(female_frame, text="頭部基因 (ZW):").grid(row=0, column=0, sticky='w')
    female_head_var = tk.StringVar()
    female_head_combo = ttk.Combobox(female_frame, textvariable=female_head_var, values=[
        "R", "r", "Ry", "b"
    ], state="readonly")
    female_head_combo.grid(row=0, column=1, padx=5, pady=2)
    female_head_combo.current(0)

    # 母鳥背部基因
    ttk.Label(female_frame, text="背部基因 (常染色體):").grid(row=1, column=0, sticky='w')
    female_back_var = tk.StringVar()
    female_back_combo = ttk.Combobox(female_frame, textvariable=female_back_var, values=[
        "G/G", "G/b", "G/Y", "b/b", "Y/Y"
    ], state="readonly")
    female_back_combo.grid(row=1, column=1, padx=5, pady=2)
    female_back_combo.current(0)

    # 母鳥胸部基因
    ttk.Label(female_frame, text="胸部基因 (常染色體):").grid(row=2, column=0, sticky='w')
    female_chest_var = tk.StringVar()
    female_chest_combo = ttk.Combobox(female_frame, textvariable=female_chest_var, values=[
        "P/P", "P/w", "w/w"
    ], state="readonly")
    female_chest_combo.grid(row=2, column=1, padx=5, pady=2)
    female_chest_combo.current(0)

    # 計算按鈕
    calculate_button = ttk.Button(root, text="計算子代顏色", command=calculate)
    calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

    # 顯示結果的文字框
    result_text = tk.Text(root, height=20, width=80)
    result_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

# 啟動 GUI
create_gui()
