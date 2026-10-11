import os
import pymupdf

def create_pdf(filename: str, pages_content: list):
    doc = pymupdf.open()
    for text in pages_content:
        page = doc.new_page(width=595, height=842) # A4 size
        rect = pymupdf.Rect(50, 50, 545, 792)
        page.insert_textbox(rect, text, fontsize=11, fontname="helv", align=pymupdf.TEXT_ALIGN_LEFT)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    doc.save(filename)
    doc.close()
    print(f"Created {filename}")

# 1. Civil Judgment
civil_p1 = """IN THE HIGH COURT OF DELHI AT NEW DELHI
R.F.A. (OS) No. 412 of 2023

RAMESH SHARMA                                       ... Appellant / Plaintiff
      Versus
MODERN REAL ESTATE DEVELOPERS PVT. LTD.             ... Respondent / Defendant

CORAM:
HON'BLE MR. JUSTICE R.K. MEHTA

JUDGMENT
1. The present regular first appeal has been filed by the Appellant, Ramesh Sharma, challenging the impugned judgment and decree passed in CS (OS) 890/2020.
2. The dispute pertains to a commercial lease agreement dated 14th January 2021 entered into between Ramesh Sharma and Modern Real Estate Developers Pvt. Ltd. for office premises located at Connaught Place, New Delhi.
3. The appellant paid an advance deposit of Rs. 25,00,000. Under clause 12 of the agreement, possession was to be delivered within 90 days. The respondent completely failed to deliver possession or refund the advance security deposit.
4. The appellant issued statutory legal notice demanding refund along with interest under Section 73 of the Indian Contract Act, 1872."""

civil_p2 = """5. The respondent in its written statement contended that force majeure conditions prevented timely delivery of the premises.
6. The primary legal issue framed by this Court is: Whether the appellant is entitled to refund and damages under Section 73 of the Indian Contract Act, 1872 and interest under Section 34 of the Code of Civil Procedure, 1908.
7. Having perused the commercial lease deed and evidence on record, the plea of force majeure is devoid of merit and an afterthought.
8. CONCLUSION AND FINAL ORDER:
The appeal is hereby allowed. The impugned decree is set aside.
The respondent Modern Real Estate Developers Pvt. Ltd. is directed to refund the principal amount of Rs. 25,00,000 along with interest at 9% per annum to the appellant Ramesh Sharma within sixty days. Suit decreed accordingly."""

create_pdf("sample_data/civil_judgment.pdf", [civil_p1, civil_p2])

# 2. Criminal Judgment
criminal_p1 = """IN THE HIGH COURT OF JUDICATURE AT BOMBAY
CRIMINAL APPELLATE JURISDICTION
CRIMINAL APPEAL NO. 789 OF 2022

STATE OF MAHARASHTRA                                ... Appellant / Prosecution
      Versus
VIKRAM DESHMUKH                                     ... Accused / Respondent

CORAM:
HON'BLE MS. JUSTICE S.A. PATIL

JUDGMENT
1. This appeal by the State of Maharashtra is directed against the judgment of acquittal dated 15th March 2022 passed by the learned Additional Sessions Judge, Pune.
2. The respondent Vikram Deshmukh was prosecuted for offenses punishable under Section 420 IPC and Section 406 IPC for alleged fraudulent inducement and criminal breach of trust relating to an investment scheme.
3. The statement of the accused was recorded under Section 313 CrPC wherein he pleaded total innocence and alleged commercial rivalry."""

criminal_p2 = """4. The prosecution examined seven witnesses to establish the charges under Section 420 IPC.
5. The crucial question before this Court is whether the prosecution proved dishonest intention at the inception of the transaction beyond reasonable doubt.
6. A careful reading of the evidence indicates that the dispute is essentially of a civil nature regarding business returns and lack of proof of deception.
7. FINAL ORDER:
There is no perversity or illegality in the findings of the learned Trial Court.
The Criminal Appeal filed by the State is dismissed. The acquittal of respondent Vikram Deshmukh under Section 420 IPC and Section 406 IPC is affirmed."""

create_pdf("sample_data/criminal_judgment.pdf", [criminal_p1, criminal_p2])

# 3. Interim Order (No final outcome)
interim_p1 = """IN THE SUPREME COURT OF INDIA
CIVIL ORIGINAL JURISDICTION
SPECIAL LEAVE PETITION (CIVIL) NO. 10244 OF 2024

GREEN PLANET CONSERVATION SOCIETY                   ... Petitioner
      Versus
UNION OF INDIA & ORS.                               ... Respondents

ORDER
1. Heard learned Senior Counsel for the Petitioner Green Planet Conservation Society and learned Solicitor General for the Union of India.
2. The petition raises vital questions concerning environmental protection under Article 21 and Article 48A of the Constitution of India in relation to the proposed highway widening in the Western Ghats eco-sensitive zone.
3. Learned Counsel for the petitioner submits that ongoing tree felling without cumulative environmental impact assessment will cause irreversible damage.
4. Issue notice to the respondents returnable within four weeks.
5. In the meantime, there shall be an interim stay on further cutting of trees in the disputed 12-kilometer stretch until the next date of hearing.
6. The matter is adjourned to 15th November 2026 for further consideration. No final order or decree is passed at this stage."""

create_pdf("sample_data/interim_order.pdf", [interim_p1])

# 4. Corrupted file
with open("sample_data/corrupted_document.pdf", "wb") as f:
    f.write(b"NOT_A_VALID_PDF_HEADER_JUST_GARBAGE_BYTES_1234567890\x00\xFF\xAA")
print("Created sample_data/corrupted_document.pdf")
