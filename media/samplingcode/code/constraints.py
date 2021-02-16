class Constraint:
    """Constraints loaded from a file."""

    def __init__(self, fname):
        """
        Construct a Constraint object from a constraints file

        :param fname: Name of the file to read the Constraint from (string)
        """
        with open(fname, "r") as f:
            lines = f.readlines()
        # Parse the dimension from the first line
        self.n_dim = int(lines[0])
        # Parse the example from the second line
        self.example = [float(x) for x in lines[1].split(" ")[0:self.n_dim]]

        # Run through the rest of the lines and compile the constraints
        self.exprs = []
        self.exprs_eval = []
        for i in range(2, len(lines)):
            # support comments in the first line
            if lines[i][0] == "#":
                continue
            self.exprs.append(compile(lines[i], "<string>", "eval"))

            dum_lines=lines[i].split()
            codeinstring=dum_lines[0]
            for i in range(1,len(dum_lines)-2):
                codeinstring=codeinstring+" "+dum_lines[i]
            self.exprs_eval.append(compile(codeinstring, "<float>", "eval"))

        return

    def get_example(self):
        """Get the example feasible vector"""
        return self.example

    def get_ndim(self):
        """Get the dimension of the space on which the constraints are defined"""
        return self.n_dim

    def apply(self, x):
        """
        Apply the constraints to a vector, returning True only if all are satisfied

        :param x: list or array on which to evaluate the constraints
        """
        for expr in self.exprs:
            if not eval(expr):
                return False
        return True

    def apply_eval(self, x):
        """
        Apply the constraints to a vector, returning the value

        :param x: list or array on which to evaluate the constraints
        """

        constr_vals=[]
        for expr in self.exprs_eval:
            constr_vals.append(eval(expr))

        return constr_vals