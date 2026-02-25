class UserNotFoundException(Exception):
    pass

class ProductNotFoundException(Exception):
    pass

class ApplicationNotFoundException(Exception):
    pass

class DuplicateEmailException(Exception):
    pass

class InvalidLoanAmountException(Exception):
    pass

class InvalidStatusTransitionException(Exception):
    pass

class InvalidRepaymentException(Exception):
    pass
