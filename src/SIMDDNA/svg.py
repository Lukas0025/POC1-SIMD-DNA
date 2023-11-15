import svgwrite

# Vytvoření nového SVG dokumentu
svg_document = svgwrite.Drawing('complementary_strands.svg', profile='tiny', size=(400, 60))

# Nukleotidy pro první vlákno
strand1 = "ATGCTAAGCTAGCTA"

# Funkce pro získání komplementárního nukleotidu
def get_complementary_base(base):
    if base == 'A':
        return 'T'
    elif base == 'T':
        return 'A'
    elif base == 'C':
        return 'G'
    elif base == 'G':
        return 'C'
    else:
        return base

# Nukleotidy pro druhé komplementární vlákno
strand2 = ''.join([get_complementary_base(base) for base in strand1])

# Barvy pro jednotlivé nukleotidy
color_map = {'A': 'blue', 'T': 'red', 'C': 'green', 'G': 'yellow'}

# Vykreslení prvního vlákna
for i, base in enumerate(strand1):

    baseSize = 30
    
    x1 = i  * baseSize
    y1 = 10
    x2 = x1 + baseSize
    y2 = 10

    svg_document.add(svgwrite.shapes.Line(start=(x1, y1), end=(x2, y2), stroke=color_map[base], stroke_width=2))
    svg_document.add(svgwrite.text.Text(base, insert=(x1 + baseSize / 2 - 12 / 2, y1), font_size=12, fill=color_map[base]))

# Uložení SVG dokumentu
svg_document.save()
