import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

def parser(text):
    if not text:
        return None

    for c in text:
        if c not in Polynomial.POSSIBLE_SUMBOLS:
            return None
    terms = []
    current = ""
    for c in text:
        if c == "+" or c == "-":
            if current:
                terms.append(current)
            current = c
        else:
            current += c
    if current:
        terms.append(current)
    
    new_coef = [0.] * Polynomial.MAX_LENGTH
    for term in terms:
        if 'x' in term:
            # accept term only of type 'coefficient'*x^'power'
            try:
                c, p = term.split('x')
            except ValueError:
                return None
            
            if not c or c == '+':
                coefficient = 1.
            elif c == '-':
                coefficient = -1.
            else:
                if (c[-1] == '*'):
                    c = c[:-1]
                try:
                    coefficient = float(c)
                except ValueError:
                    return None
                    
            if not p:
                power = 1
            else:
                try:
                    power = int(p[1:])
                except ValueError:
                    return None

            if power >= Polynomial.MAX_LENGTH:
                # cannot have such power in our polinomial
                return 
            new_coef[power] += coefficient
        else:
            # free coefficient
            try:
                new_coef[0] += float(term)
            except ValueError:
                return None
    return Polynomial(new_coef)

class Polynomial:
    MAX_LENGTH = 4 # a*x^0 + b*x^1 + c*x^2 + d*x^3
    POSSIBLE_SUMBOLS = "0123456789.*/+-x^"

    def __init__(self, coef=[]):
        self.coef = coef
        if not coef:
            self.reset()
    
    def reset(self):
        # clear list of coefficients
        self.coef = [0.] * Polynomial.MAX_LENGTH

    def is_zero(x: float):
        return abs(x) < 0.000001
        
    def sign(x):
        if x > 0:
            return 1
        return -1

    def to_str(self):
        ret = ""
        x = ""
        for p, c in enumerate(self.coef):
            # p - power, c - coefficient
            if isinstance(c, str):
                ret += c # case of 'C' in integral
            elif not Polynomial.is_zero(c):
                ret += f"{c:+.3f}{x}"
            if not p:
                x = '*x'
            else:
                x = f"*x^{p+1}"

        if ret and ret[0] == '+':
            ret = ret[1:]
        if not ret:
            ret = "0"
        return ret
        
    def get_power(self):
        ret = 0
        for i, coef in enumerate(self.coef):
            if not Polynomial.is_zero(coef):
                ret = i
        return ret

    def get_zero_points(self):
        ret = list()
        p = self.get_power()
        if p == 1:
            ret = [-self.coef[0] / self.coef[1]]
        elif p == 2:
            a = self.coef[2]
            b = self.coef[1]
            c = self.coef[0]
            D = b*b - 4*a*c
            if Polynomial.is_zero(D):
                ret = [-b/(2*a)]
            elif D > 0:
                ret = [(-b + D**0.5)/(2*a),
                       (-b - D**0.5)/(2*a)]
        return ret

    def get_at_point(self, x):
        ret = 0.
        p = 1.
        for coef in self.coef:
            ret += coef*p
            p *= x
        return ret

    def get_y(self, lin):
        if isinstance(lin, (float, int)):
            # get at one point
            return self.get_at_point(lin)
        # get at many points
        return [self.get_at_point(y) for y in lin]

    def get_derivative(self):
        deriv = Polynomial([self.coef[i]*i for i in range(1, len(self.coef))])
        return deriv

    def get_integral(self):
        integral = Polynomial(["C"] + [self.coef[i]/(i+1) for i in range(len(self.coef))])
        return integral

    def get_intervals(self):
        # return [ascending_intervals, descending_intervals]
        asc = []
        desc = []
        deriv = self.get_derivative()
        if deriv.get_power() == 0:
            if deriv.coef[0] > 0:
                asc.append([float("-INF"), float("+INF")])
            else:
                desc.append([float("-INF"), float("+INF")])

        elif deriv.get_power() > 0:
            crit_points = deriv.get_zero_points()
            intervals = [float("-INF")] + crit_points + [float("INF")]
            for i in range(len(intervals)-1):
                l = intervals[i]
                r = intervals[i+1]
                sign = 1
                if l == float("-INF") and r == float("INF"):
                    sign = Polynomial.sign(deriv.get_y(0))
                elif l == float("-INF"):
                    sign = Polynomial.sign(deriv.get_y(2*r-10))
                elif r == float("INF"):
                    sign = Polynomial.sign(deriv.get_y(2*l+10))
                else:
                    sign = Polynomial.sign(deriv.get_y((l+r)/2))
                
                if sign == 1:
                    asc.append((l, r))
                else:
                    desc.append((l, r))
        return [asc, desc]

    def get_info(self):
        ret = dict()
        for s in ("Polinomial", "Derivative", "Integral", "Critical points", "Ascending intervals", "Descending intervals", "Convex intervals", "Concave intervals"):
            ret[s] = "No"

        ret["Polinomial"] = self.to_str()
        ret["Integral"] = self.get_integral().to_str()

        deriv = self.get_derivative()
        ret["Derivative"] = deriv.to_str()
        crit_points = deriv.get_zero_points()

        if crit_points:
            ret["Critical points"] = ", ".join(f"{i:.3f}" for i in crit_points)

        if self.get_power() > 0:
            asc, desc = self.get_intervals()
            intervals_to_str = lambda cur: ", ".join(f"({l:.3f}, {r:.3f})" for l, r in cur)
            if asc:
                ret["Ascending intervals"] = intervals_to_str(asc)
            if desc:
                ret["Descending intervals"] = intervals_to_str(desc)
            if self.get_power() > 1:
                convex, concave = deriv.get_intervals()
                if convex:
                    ret["Convex intervals"] = intervals_to_str(convex)
                if concave:
                    ret["Concave intervals"] = intervals_to_str(concave)
        return ret



class Main():
    FONT = ("Arial", 12)
    INFO_NAMES = ("Derivative", "Integral", "Critical points", "Ascending intervals", "Descending intervals", "Convex intervals", "Concave intervals")

    def __init__(self):
        
        self.function = None

        window = tk.Tk()
        window.title("Endterm")

        frm_graph = tk.Frame()
        self.plt_fig = Figure(figsize=(6.5, 5), dpi=100)
        self.plt_canvas = FigureCanvasTkAgg(self.plt_fig, master=frm_graph)
        self.plt_toolbar = NavigationToolbar2Tk(self.plt_canvas, frm_graph)
        self.plt_toolbar.update()
        self.plt_canvas.get_tk_widget().pack()

        # Naming rules
        # lbl = Label
        # bnt = Button
        # ent = Entry
        # frm = Frame

        frm_input = tk.Frame(padx=5, pady=5)

        lbl_help = tk.Label(master=frm_input, text="Accept only polinomials up to third power of the form:\n sum of 'coefficient'*x^'power'", font=Main.FONT, bg="gainsboro", width=60, height=2)
        lbl_help.grid(column=0, row=0, padx=5, pady=5, columnspan=3)

        self.ent_input = tk.Entry(master=frm_input, bg="gainsboro", width=30, font=Main.FONT)
        self.ent_input.grid(column=0, row=1, padx=5, pady=5)
                    

        self.btn_input = tk.Button(master=frm_input, text="Enter", font=Main.FONT, bg="gainsboro", width=10, command=self.update)
        self.btn_input.grid(column=1, row=1, padx=5, pady=5)
            
        self.lbl_input = tk.Label(master=frm_input, text="Press button 'Enter'", font=Main.FONT, bg="gainsboro", width=30, height=1)
        self.lbl_input.grid(column=2, row=1, padx=5, pady=5)

        frm_info = tk.Frame(padx=5, pady=5)

        self.lbls_info = []

        for i, name in enumerate(Main.INFO_NAMES):
            lbl_name = tk.Label(master=frm_info, text=name, font=Main.FONT, bg="gainsboro")
            lbl_name.grid(column=0, row=3*i, padx=5, pady=5)
            lbl_info = tk.Label(master=frm_info, text="", font=Main.FONT, bg="gainsboro")
            lbl_info.grid(column=0, row=3*i+1, padx=5, pady=5)
            self.lbls_info.append([lbl_name, lbl_info])

        frm_graph.grid(column=0, row=0)
        frm_input.grid(column=0, row=1)
        frm_info.grid(column=1, row=0)

        window.mainloop()

    def display(self, xlim=(-100, 100)):
        self.plt_fig.clf()
        if self.function == None:
            return
        subplot = self.plt_fig.add_subplot(111)
        subplot.set_xlim(xlim)
        subplot.set_xlabel("X")
        subplot.set_ylabel("Y")

        X = [i/10 for i in range(xlim[0]*10, xlim[1]*10)]
        Y = self.function.get_y(X)
        subplot.plot(X, Y, color="black", linewidth=2)

        self.plt_canvas.draw()

    def update(self):
        text = self.ent_input.get()
        self.function = parser(text)
        if self.function == None:
            return

        for name, info in self.lbls_info:
            info["text"] = ''
        self.lbl_input["text"] = "Wrong input"

        if self.function != None:
            info = self.function.get_info()
            self.lbl_input["text"] = info["Polinomial"]
            for i, name in enumerate(Main.INFO_NAMES):
                # update information about function
                self.lbls_info[i][1]["text"] = info.get(name, '')

        self.display()

if __name__ == "__main__":
    Main()  