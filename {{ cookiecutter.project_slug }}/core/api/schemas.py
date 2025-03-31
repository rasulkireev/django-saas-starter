from ninja import Schema


class SubmitFeedbackIn(Schema):
    feedback: str
    page: str

class SubmitFeedbackOut(Schema):
    success: bool
    message: str
