from google.cloud import recaptchaenterprise_v1
from google.cloud.recaptchaenterprise_v1 import Assessment

def validate_recaptcha(token, project_id, site_key):
    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()
    assessment = recaptchaenterprise_v1.Assessment(
        event=recaptchaenterprise_v1.Event(
            token=token,
            site_key=site_key,
        )
    )
    request = recaptchaenterprise_v1.CreateAssessmentRequest(
        parent=f"projects/{project_id}",
        assessment=assessment,
    )
    response = client.create_assessment(request)

    # Check if the token is valid and has a low risk score
    if not response.token_properties.valid:
        raise ValueError("Invalid reCAPTCHA token.")
    if response.risk_analysis.score < 0.5:  # Customize the threshold as needed
        raise ValueError("reCAPTCHA verification failed (high risk).")

    return True


def create_assessment(
    project_id: str, recaptcha_key: str, token: str, recaptcha_action: str
) -> Assessment:

    client = recaptchaenterprise_v1.RecaptchaEnterpriseServiceClient()

    # Set the properties of the event to be tracked.
    event = recaptchaenterprise_v1.Event()
    event.site_key = recaptcha_key
    event.token = token

    assessment = recaptchaenterprise_v1.Assessment()
    assessment.event = event

    project_name = f"projects/{project_id}"

    # Build the assessment request.
    request = recaptchaenterprise_v1.CreateAssessmentRequest()
    request.assessment = assessment
    request.parent = project_name

    response = client.create_assessment(request)

    # Check if the token is valid.
    if not response.token_properties.valid:
        print(
            "The CreateAssessment call failed because the token was "
            + "invalid for the following reasons: "
            + str(response.token_properties.invalid_reason)
        )
        raise ValueError("Invalid reCAPTCHA token.")
        # return

    # Check if the expected action was executed.
    if response.token_properties.action != recaptcha_action:
        print(
            "The action attribute in your reCAPTCHA tag does"
            + "not match the action you are expecting to score"
        )
        return
    else:
        # Get the risk score and the reason(s).
        # For more information on interpreting the assessment, see:
        # https://cloud.google.com/recaptcha-enterprise/docs/interpret-assessment
        for reason in response.risk_analysis.reasons:
            print(reason)
        print(
            "The reCAPTCHA score for this token is: "
            + str(response.risk_analysis.score)
        )
        # Get the assessment name (ID). Use this to annotate the assessment.
        assessment_name = client.parse_assessment_path(response.name).get("assessment")
        print(f"Assessment name: {assessment_name}")
    return response