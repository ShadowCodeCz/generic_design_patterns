import re
import pytest
import generic_design_patterns as gdp

# Test Input For Condition


class Form(object):
    def __init__(self, label, text=""):
        self.label = label
        self.text = text

    def __repr__(self):
        return "%s, %s" % (self.label, self.text)


name_homer_simpson = Form("nickname", "Homer Simpson")
name_abe_simpson = Form("nickname", "Abe Simpson")
name_montgomery_burns = Form("nickname", "Montgomery Burns")
valid_homer_email = Form("mail", "homer@maxi.power")
invalid_homer_email = Form("mail", "homermaxi.power")


# Test Conditions


class IsMandatory(gdp.specification.Condition):
    mandatory_forms = ["nickname", "mail", "password"]

    def is_satisfied(self, form):
        return form.label in self.mandatory_forms


class IsEmpty(gdp.specification.Condition):
    def is_satisfied(self, form):
        return form.text.strip() == ""


class IsValidMail(gdp.specification.Condition):
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    def is_satisfied(self, form):
        return (form.label == "mail") & self._is_mail_valid(form)

    def _is_mail_valid(self, form):
        return True if re.match(self.email_pattern, form.text) else False


class IsHomer(gdp.specification.Condition):
    def is_satisfied(self, form):
        return "Homer" in form.text


class IsSimpson(gdp.specification.Condition):
    def is_satisfied(self, form):
        return "Simpson" in form.text

# Test Inputs


class ExpectedConditionEvaluation:
    def __init__(self):
        self.result = None
        self.results = []


class TInput:
    def __init__(self):
        self.form = None
        self.condition = None
        self.expectation = ExpectedConditionEvaluation()

    @property
    def id(self):
        return "%s [%s]" % (repr(self.condition), repr(self.form))


tis = []

ti = TInput()
ti.form = name_homer_simpson
ti.condition = IsMandatory()
ti.expectation.result = True
ti.expectation.results += [gdp.specification.ConditionEvaluationResult("IsMandatory", True)]
tis.append(ti)

ti = TInput()
ti.form = name_homer_simpson
ti.condition = IsEmpty()
ti.expectation.result = False
ti.expectation.results += [gdp.specification.ConditionEvaluationResult("IsEmpty", False)]
tis.append(ti)

ti = TInput()
ti.form = name_homer_simpson
ti.condition = ~IsEmpty()
ti.expectation.result = True
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(not IsEmpty)", True),
    gdp.specification.ConditionEvaluationResult("IsEmpty", False)
]
tis.append(ti)

ti = TInput()
ti.form = name_homer_simpson
ti.condition = ~IsHomer()
ti.expectation.result = False
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(not IsHomer)", False),
    gdp.specification.ConditionEvaluationResult("IsHomer", True)
]
tis.append(ti)

ti = TInput()
ti.form = valid_homer_email
ti.condition = IsValidMail() & IsMandatory()
ti.expectation.result = True
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(IsValidMail and IsMandatory)", True),
    gdp.specification.ConditionEvaluationResult("IsValidMail", True),
    gdp.specification.ConditionEvaluationResult("IsMandatory", True)
]
tis.append(ti)

ti = TInput()
ti.form = invalid_homer_email
ti.condition = IsValidMail() & IsMandatory()
ti.expectation.result = False
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(IsValidMail and IsMandatory)", False),
    gdp.specification.ConditionEvaluationResult("IsValidMail", False),
    gdp.specification.ConditionEvaluationResult("IsMandatory", True)
]
tis.append(ti)

ti = TInput()
ti.form = name_abe_simpson
ti.condition = IsHomer() | IsSimpson()
ti.expectation.result = True
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(IsHomer or IsSimpson)", True),
    gdp.specification.ConditionEvaluationResult("IsHomer", False),
    gdp.specification.ConditionEvaluationResult("IsSimpson", True)
]
tis.append(ti)

ti = TInput()
ti.form = name_montgomery_burns
ti.condition = IsHomer() | IsSimpson()
ti.expectation.result = False
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(IsHomer or IsSimpson)", False),
    gdp.specification.ConditionEvaluationResult("IsHomer", False),
    gdp.specification.ConditionEvaluationResult("IsSimpson", False)
]
tis.append(ti)

ti = TInput()
ti.form = name_homer_simpson
ti.condition = IsHomer() ^ IsSimpson()
ti.expectation.result = False
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(IsHomer xor IsSimpson)", False),
    gdp.specification.ConditionEvaluationResult("IsHomer", True),
    gdp.specification.ConditionEvaluationResult("IsSimpson", True)
]
tis.append(ti)

ti = TInput()
ti.form = name_abe_simpson
ti.condition = IsHomer() ^ IsSimpson()
ti.expectation.result = True
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(IsHomer xor IsSimpson)", True),
    gdp.specification.ConditionEvaluationResult("IsHomer", False),
    gdp.specification.ConditionEvaluationResult("IsSimpson", True)
]
tis.append(ti)

ti = TInput()
ti.form = name_homer_simpson
ti.condition = IsHomer() ^ IsSimpson() & IsMandatory()
ti.expectation.result = False
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(IsHomer xor (IsSimpson and IsMandatory))", False),
    gdp.specification.ConditionEvaluationResult("(IsSimpson and IsMandatory)", True),
    gdp.specification.ConditionEvaluationResult("IsHomer", True),
    gdp.specification.ConditionEvaluationResult("IsSimpson", True),
    gdp.specification.ConditionEvaluationResult("IsMandatory", True)
]
tis.append(ti)

ti = TInput()
ti.form = name_abe_simpson
ti.condition = (IsHomer() | IsSimpson()) & (IsMandatory() & ~IsEmpty())
ti.expectation.result = True
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("((IsHomer or IsSimpson) and (IsMandatory and (not IsEmpty)))", True),
    gdp.specification.ConditionEvaluationResult("(IsMandatory and (not IsEmpty))", True),
    gdp.specification.ConditionEvaluationResult("(IsHomer or IsSimpson)", True),
    gdp.specification.ConditionEvaluationResult("(not IsEmpty)", True),
    gdp.specification.ConditionEvaluationResult("IsHomer", False),
    gdp.specification.ConditionEvaluationResult("IsSimpson", True),
    gdp.specification.ConditionEvaluationResult("IsMandatory", True),
    gdp.specification.ConditionEvaluationResult("IsEmpty", False)
]
tis.append(ti)

ti = TInput()
ti.form = name_abe_simpson
ti.condition = ~((IsHomer() | IsSimpson()) & (IsMandatory() & ~IsEmpty()))
ti.expectation.result = False
ti.expectation.results += [
    gdp.specification.ConditionEvaluationResult("(not ((IsHomer or IsSimpson) and (IsMandatory and (not IsEmpty))))", False),
    gdp.specification.ConditionEvaluationResult("((IsHomer or IsSimpson) and (IsMandatory and (not IsEmpty)))", True),
    gdp.specification.ConditionEvaluationResult("(IsMandatory and (not IsEmpty))", True),
    gdp.specification.ConditionEvaluationResult("(IsHomer or IsSimpson)", True),
    gdp.specification.ConditionEvaluationResult("(not IsEmpty)", True),
    gdp.specification.ConditionEvaluationResult("IsHomer", False),
    gdp.specification.ConditionEvaluationResult("IsSimpson", True),
    gdp.specification.ConditionEvaluationResult("IsMandatory", True),
    gdp.specification.ConditionEvaluationResult("IsEmpty", False)
]
tis.append(ti)

ids = [ti.id for ti in tis]


# Tests

@pytest.mark.parametrize("ti", tis, ids=ids)
def test_condition_evaluation(ti):
    result = ti.condition(ti.form)
    assert result == ti.expectation.result


@pytest.mark.parametrize("ti", tis, ids=ids)
def test_condition_results(ti):
    results = ti.condition.evaluate(ti.form)
    assert len(results) == len(ti.expectation.results)

    for expected_result in ti.expectation.results:
        assert expected_result in results

