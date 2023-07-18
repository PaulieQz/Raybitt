import math
import sympy
from nextcord.ext import commands



class maths(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # mapping from special math characters to their sympy representation
        self.MATH_SYMBOLS = {
            "²": "**2",
            "³": "**3",
            "⁴": "**4",
            "⁵": "**5",
            "⁶": "**6",
            "⁷": "**7",
            "⁸": "**8",
            "⁹": "**9",
            "√": "sqrt",
            "π": "pi",
            "÷": "/",
            "×": "*",
            "•": "*",
        }

    @commands.command()
    async def square(self, ctx, num: float):
        result = num * num
        await ctx.send(f"The square of {num} is {result}")

    @commands.command()
    async def cube(self, ctx, num: float):
        result = num ** 3
        await ctx.send(f"The cube of {num} is {result}")

    @commands.command()
    async def factorial(self, ctx, num: int):
        result = math.factorial(num)
        await ctx.send(f"The factorial of {num} is {result}")

    @commands.command()
    async def simplify(self, ctx, expression: str):
        try:
            expr = sympy.sympify(expression)
            simplified_expr = sympy.simplify(expr)
            await ctx.send(f"The simplified expression is: {simplified_expr}")
        except sympy.SympifyError:
            await ctx.send("Invalid expression. Please provide a valid mathematical expression.")

    @commands.command()
    async def solve(self, ctx, equation: str):
        try:
            # replace special math characters with their sympy representation
            for symbol, sympy_repr in self.MATH_SYMBOLS.items():
                equation = equation.replace(symbol, sympy_repr)

            # check if the equation contains an equals sign
            if "=" in equation:
                # split the equation into left and right parts
                left, right = equation.split("=")
                # solve the equation
                x = sympy.symbols('x')
                expr = sympy.sympify(f"({left}) - ({right})")
                solutions = sympy.solve(expr, x)
                await ctx.send(f"The solution(s) for the equation {equation} is/are: {solutions}")
            else:
                # evaluate the arithmetic operation
                result = sympy.sympify(equation).evalf()
                await ctx.send(f"The result of {equation} is: {result}")
        except (sympy.SympifyError, ValueError):
            await ctx.send("Invalid input. Please provide a valid mathematical equation or arithmetic operation.")

    @commands.command()
    async def solve_help(self, ctx):
        help_text = """
    Here's how to use the !solve command:
    
    - Arithmetic operations:
        - Addition: `+` (e.g., `1+2`)
        - Subtraction: `-` (e.g., `3-2`)
        - Multiplication: `*` or `•` (e.g., `2*2` or `2•2`)
        - Division: `/` or `÷` (e.g., `4/2` or `4÷2`)
        - Exponentiation: `**` or superscripts (e.g., `2**3` or `2³`)
    
    - Square roots: Use the `sqrt` function (e.g., `sqrt(4)`)
    
    - Pi: Use `pi` or `π`
    
    - Equations: Use `=` to define an equation (e.g., `x=2` or `x**2 - 3*x + 2 = 0`)
    
    Remember, the !solve command can evaluate arithmetic expressions (like `1+2*3`) and solve equations (like `x=2` or `x**2 - 3*x + 2 = 0`).
        """
        await ctx.send(help_text)

    @commands.command()
    async def derivative(self, ctx, expression: str):
        try:
            x = sympy.symbols('x')
            expr = sympy.sympify(expression)
            derivative = sympy.diff(expr, x)
            await ctx.send(f"The derivative of {expression} is: {derivative}")
        except sympy.SympifyError:
            await ctx.send("Invalid expression. Please provide a valid mathematical expression.")

    @commands.command()
    async def integral(self, ctx, expression: str):
        try:
            x = sympy.symbols('x')
            expr = sympy.sympify(expression)
            integral = sympy.integrate(expr, x)
            await ctx.send(f"The integral of {expression} is: {integral}")
        except sympy.SympifyError:
            await ctx.send("Invalid expression. Please provide a valid mathematical expression.")

    @commands.command()
    async def quadratic_equation(self, ctx, a: float, b: float, c: float):
        discriminant = b ** 2 - 4 * a * c

        if discriminant > 0:
            x1 = (-b + math.sqrt(discriminant)) / (2 * a)
            x2 = (-b - math.sqrt(discriminant)) / (2 * a)
            await ctx.send(f"The solutions for the quadratic equation are: x1 = {x1}, x2 = {x2}")
        elif discriminant == 0:
            x = -b / (2 * a)
            await ctx.send(f"The solution for the quadratic equation is: x = {x}")
        else:
            await ctx.send("The quadratic equation has no real solutions.")

    @commands.command()
    async def pythagorean_theorem(self, ctx, a: float, b: float):
        c = math.sqrt(a ** 2 + b ** 2)
        await ctx.send(f"The length of the hypotenuse is: {c}")

    @commands.command()
    async def prime_factorization(self, ctx, num: int):
        factors = []
        while num % 2 == 0:
            factors.append(2)
            num = num // 2
        for i in range(3, int(math.sqrt(num)) + 1, 2):
            while num % i == 0:
                factors.append(i)
                num = num // i
        if num > 2:
            factors.append(num)
        await ctx.send(f"The prime factorization of {num} is: {factors}")


def setup(bot):
    bot.add_cog(maths(bot))
