"""The small steps within a lead's stage -- DEC-050, FR-CRM-001.

The owner's client works leads through a sheet of stages, each with smaller
steps beside it: at Initial Contact the WhatsApp sent, the email sent, the cold
call, the introductory meeting. The stages became the Lead's business status
(business_status.model.LEAD); the steps are its Stage Detail, which offers only
the current stage's steps and is cleared whenever the stage moves on.

Row 5 of the sheet -- Qualified, Potential Customer, Not Qualified -- is the
outcome of qualifying, so those are statuses of their own rather than details.
"""

#: Stage -> its steps, in the sheet's order. A stage not listed has none.
STAGE_DETAILS = {
	"Initial Contact": ["WhatsApp Sent", "Email Sent", "Cold Call", "Introductory Meeting"],
	"Requirement Pending": ["Courtesy Meeting", "Courtesy Call"],
	"Requirement Received": ["Requirement Clarification", "Requirement Confirmed"],
}


def details_for(stage):
	return STAGE_DETAILS.get(stage, [])
