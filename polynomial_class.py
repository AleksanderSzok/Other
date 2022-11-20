class Polynominal:
    def __init__(self, *args):
        if len(args) == 0:
            setattr(self, "attr0", 0)
        else:
            length = len(args) - 1
            tmp = args[-1]
            while tmp == 0 and length > 0:
                if args[length] != 0:
                    tmp = args[length]
                    length += 1
                length -= 1

            for idx, item in enumerate(args[: length + 1]):
                setattr(self, "attr{}".format(idx), item)

    def get_degree(self):
        return len(self.__dict__) - 1

    @classmethod
    def from_iterable(cls, iterable):
        return cls(*iterable)

    def __call__(self, arg):
        tmp = 0
        for num, key in enumerate(self.__dict__.keys()):
            tmp += getattr(self, key) * arg**num
        return tmp

    def __eq__(self, other):
        if self.__dict__ == other.__dict__:
            return True
        else:
            return False

    def __add__(self, other):
        length = max(len(self.__dict__), len(other.__dict__))
        one = list(self.__dict__.values())
        two = list(other.__dict__.values())
        if len(one) > len(two):
            two.extend([0] * (length - len(two)))
        elif len(one) < len(two):
            one.extend(([0] * (length - len(one))))
        return self.from_iterable([sum(element) for element in zip(one, two)])

    def __mul__(self, other):
        one = list(self.__dict__.values())
        two = list(other.__dict__.values())
        degree = len(one) + len(two) - 1
        output = [0] * degree
        for i in range(len(one)):
            for j in range(len(two)):
                tmp = one[i] * two[j]
                output[i + j] += tmp
        return self.from_iterable(output)

    def __str__(self):
        list_of_coefficients = []
        for num, key in enumerate(self.__dict__.keys()):
            if getattr(self, key) == 1:
                if num == 0:
                    list_of_coefficients.append(f"1 ")
                elif num == 1:
                    list_of_coefficients.append(f"+ x ")
                else:
                    list_of_coefficients.append(f"+ x^{num} ")
            elif getattr(self, key) == -1:
                if num == 0:
                    list_of_coefficients.append(f"-1 ")
                elif num == 1:
                    list_of_coefficients.append(f"- x ")
                else:
                    list_of_coefficients.append(f"- x^{num} ")
            elif int(getattr(self, key)) > 1:
                if num == 0:
                    list_of_coefficients.append(f"+ {getattr(self, key)} ")
                elif num == 1:
                    list_of_coefficients.append(f"+ {getattr(self, key)}x ")
                else:
                    list_of_coefficients.append(f"+ {getattr(self, key)}x^{num} ")
            elif int(getattr(self, key)) < -1:
                negative_coeff = -int(getattr(self, key))
                if num == 0:
                    list_of_coefficients.append(f"- {negative_coeff} ")
                elif num == 1:
                    list_of_coefficients.append(f"- {negative_coeff}x ")
                else:
                    list_of_coefficients.append(f"- {negative_coeff}x^{num} ")
        return "".join(list_of_coefficients).lstrip("+").lstrip().rstrip()
