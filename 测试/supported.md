#! https://zhuanlan.zhihu.com/p/695235678

# KaTeX 支持测试

来源：
https://katex.org/docs/supported.html

https://github.com/KaTeX/KaTeX/blob/main/docs/supported.md

在 vscode 上，大部分函数都支持。

下面是测试结果

$v, w, \nu, \omega$

$$
M_{\mathrm{cg}} = \underbrace{M_{\mathrm{f}}}_{\text{机身贡献}} +\underbrace{M_{\mathrm{sc},\mathrm{w}} + L_{\mathrm{w}}x_{\mathrm{a}}}_{\text{机载贡献}} + \underbrace{M_{\mathrm{sc},\mathrm{t}} - L_{\mathrm{t}}l_{\mathrm{t}}}_{\text{平地贡献}}
$$

$$
f(n)=
\begin{cases}
\frac{n}{2},&\text{if $n$ is even}\\[5ex]
3n+1,&\text{if $n$ is odd}
\end{cases}
$$

$$
T\mathrm{cos}\varepsilon - D - W\mathrm{sin}\gamma = \cancel{\frac{W}{g} \frac{\mathrm{d}V}{\mathrm{d}t}}
$$

$$
\cancel{T\mathrm{sin}\varepsilon} + L - W\mathrm{cos}\gamma = \cancel{\frac{W}{g} \frac{V^{2}}{R}}
$$

$$
u_{\substack{\max\\\min}}=\sqrt{z\pm\sqrt{z^{2}-1}}
$$

## Accents

$a'$ `a'`  

$\tilde{a}$ `\tilde{a}`

$\mathring{g}$ `\mathring{g}`


$a''$ `a''`

$\widetilde{ac}$ `\widetilde{ac}`  

$\overgroup{AB}$ `\overgroup{AB}`


$a^{\prime}$ `a^{\prime}`

$\utilde{AB}$ `\utilde{AB}`

$\utilde{A}$

$\undergroup{AB}$ `\undergroup{AB}`


$\acute{a}$ `\acute{a}`

$\vec{F}$ `\vec{F}`

$\Overrightarrow{AB}$ `\Overrightarrow{AB}`


$\bar{y}$ `\bar{y}`

$\overleftarrow{AB}$ `\overleftarrow{AB}`

$\overrightarrow{AB}$ `\overrightarrow{AB}`


$\breve{a}$ `\breve{a}`

$\underleftarrow{AB}$ `\underleftarrow{AB}`

$\underrightarrow{AB}$ `\underrightarrow{AB}`


$\check{a}$ `\check{a}`

$\overleftharpoon{ac}$ `\overleftharpoon{ac}`  

$\overrightharpoon{ac}$ `\overrightharpoon{ac}`


$\dot{a}$ `\dot{a}`

$\overleftrightarrow{AB}$ `\overleftrightarrow{AB}`  

$\overbrace{AB}$ `\overbrace{AB}`


$\ddot{a}$ `\ddot{a}`  

$\underleftrightarrow{AB}$ `\underleftrightarrow{AB}`

$\underbrace{AB}$ `\underbrace{AB}`


$\grave{a}$ `\grave{a}`

$\overline{AB}$ `\overline{AB}`

$\overlinesegment{AB}$ `\overlinesegment{AB}`


$\hat{\theta}$ `\hat{\theta}`

$\underline{AB}$ `\underline{AB}`  

$\underlinesegment{AB}$ `\underlinesegment{AB}`


$\widehat{ac}$ `\widehat{ac}`

$\widecheck{ac}$ `\widecheck{ac}`  

$\underbar{X}$ `\underbar{X}`



$\text{\'{a}}$ `\'{a}`

$\text{\~{a}}$ `\~{a}`

$\text{\.{a}}$ `\.{a}`

$\text{\H{a}}$ `\H{a}`

$\text{\`{a}}$ <code>\\`{a}</code>

$\text{\={a}}$ `\={a}`

$\text{\"{a}}$ `\"{a}`

$\text{\v{a}}$ `\v{a}`


$\text{\^{a}}$ `\^{a}`

$\text{\u{a}}$ `\u{a}`

$\text{\r{a}}$ `\r{a}`


$\phase{-78^\circ}$

${A \atop B}R$

$\ket{\psi}$

$\braket{\phi|\psi}$

$\dbinom{n}{k}$

${n \choose k}$

$\Set{ x | x<\frac 1 2 }$

$\displaystyle \sum_{\substack{0<i<m\\0<j<n}}$

$$
\def\arraystretch{1.5}
\begin{array}{c:c:c}
a & b & c \\ \hline
d & e & f \\
\hdashline
g & h & i
\end{array}
$$
