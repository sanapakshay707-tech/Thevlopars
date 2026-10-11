**SOFTWARE REQUIREMENTS SPECIFICATION (SRS)**

**Proof Keeper**

**AI-Assisted Court Document Review and Similar Case Finder**

**Project Domain:** Legal Technology — Indian Judicial Documents
**Project Type:** Hackathon Prototype
**Version:** 1.0
**Status:** Proposed
**Prepared for:** Hackathon Project Team
**Target Implementation Time:** 8 Hours
**Target Platform:** Windows Desktop / Local Web Application

**Document Control**

| **Field** | **Description** |
| --- | --- |
| Document title | Software Requirements Specification — Proof Keeper |
| Version | 1.0 |
| Project name | Proof Keeper |
| Document status | Initial baseline |
| Intended audience | Developers, testers, evaluators, and project stakeholders |
| Primary users | Court clerks, law students, junior lawyers, and citizens |
| Development approach | Rapid prototyping |
| Reference framework | IEEE-style SRS structure, informed by ISO/IEC/IEEE 29148 principles |

**Revision History**

| **Version** | **Date** | **Description** |
| --- | --- | --- |
| 1.0 | 11 October 2026 | Initial SRS for the hackathon prototype |

**1. Introduction**

**1.1 Purpose**

This Software Requirements Specification defines the functional and non-functional requirements, system architecture, interfaces, data requirements, constraints, and testing criteria for Proof Keeper.

Proof Keeper is an AI-assisted application intended to simplify the review and organization of lengthy Indian court judgments and orders. It allows users to upload a PDF, extract important legal information, view a structured case summary, and discover potentially related judgments from a preloaded collection.

This document will serve as the primary reference for implementing and testing the project within the hackathon's limited development time.

**1.2 Problem Statement**

Indian courts produce large volumes of judgments, orders, and other legal documents. These documents frequently contain dense legal language, complex sentence structures, statutory references, procedural history, and lengthy factual narratives.

Court clerks, junior lawyers, law students, and citizens may need to read extensive documents to determine:

- Whether a case is civil, criminal, or another supported category.

- Who the parties are.

- Which Acts and statutory provisions are mentioned.

- What legal issues and important facts are involved.

- What the court ultimately decided.

- Whether other documents in an available collection discuss similar issues.

Manual review can consume significant time. Simple keyword searches may also fail to identify documents that discuss similar legal issues using different terminology.

Proof Keeper aims to reduce the initial document-review burden by automatically organizing available information and identifying potentially related judgments, while retaining access to the original source material.

**1.3 Project Objectives**

The objectives are to:

- Enable users to upload multipage court judgment PDFs.

- Extract readable text from uploaded documents.

- Automatically identify important case information.

- Present a concise, structured case summary.

- Identify legal Acts, sections, parties, legal issues, and the reported outcome.

- Find potentially related judgments from a predefined collection.

- Explain the reasons for each similarity match.

- Display original source passages and page references where available.

- Clearly distinguish extracted facts from uncertain or missing information.

- Demonstrate the feasibility of the solution using a small, curated dataset.

**1.4 Scope**

**In scope — Minimum Viable Product (MVP)**

- PDF upload and validation.

- Text extraction from text-based PDFs.

- Basic support for identifying scanned PDFs.

- Case category classification.

- Extraction of parties, legal provisions, legal issues, key facts, and outcome.

- Concise case summary.

- Similar Case Finder using semantic and lexical similarity.

- Comparison against a preloaded collection of approximately 20–50 judgments.

- Ranking and display of the top five potentially related cases.

- Match explanations and source references.

- Basic error handling.

- Manual verification of extracted results.

**Optional features**

- OCR processing using Tesseract.

- Local language-model assistance using Ollama and Qwen2.5 3B.

- Interactive charts using Plotly.

- Search and filtering by case category or Act.

- Downloading a structured analysis report.

- Adding new judgments to the searchable collection through an administrative workflow.

Optional features should only be implemented after the core workflow functions reliably.

**1.5 Out of Scope**

The initial prototype will not:

- Replace a lawyer, judge, or legal researcher.

- Provide binding legal advice.

- Determine whether a precedent is legally binding or applicable.

- Predict court decisions or guarantee case outcomes.

- Cover every Indian court or legal database.

- Guarantee extraction accuracy for every document.

- Automatically download judgments from external websites.

- Train a new legal foundation model.

- Provide production-grade multi-user access control.

- Perform comprehensive legal research across all publicly available judgments.

- Guarantee support for every Indian language or handwritten document.

**1.6 Intended Audience**

This specification is intended for:

- Developers implementing the application.

- Testers evaluating the system.

- Hackathon judges assessing the solution.

- Project team members planning the implementation.

- Stakeholders reviewing the proposed functionality and limitations.

**2. Definitions and Abbreviations**

| **Term** | **Definition** |
| --- | --- |
| AI | Artificial Intelligence |
| OCR | Optical Character Recognition, used to extract text from images |
| PDF | Portable Document Format |
| SRS | Software Requirements Specification |
| MVP | Minimum Viable Product |
| LLM | Large Language Model |
| Embedding | A numerical vector representing the meaning of a text passage |
| Semantic similarity | A measure of how closely two texts are related in meaning |
| TF-IDF | Term Frequency–Inverse Document Frequency, a method for representing text based on word importance |
| Cosine similarity | A mathematical measure used to compare vectors |
| Legal provision | A section, article, rule, or other statutory reference |
| Judgment | A court's decision or written judicial reasoning |
| Case outcome | The decision or disposition recorded in a judgment or order |
| Source evidence | Original text and page references supporting an extracted field |
| Similar Case Finder | A module that ranks potentially related judgments |
| Curated dataset | A selected collection of judgment documents prepared for the prototype |
| Precision@5 | The proportion of the top five retrieved results judged relevant |

**3. Overall Description**

**3.1 Product Perspective**

Proof Keeper is a standalone local web application. Users interact with it through a browser, while the application processes documents using Python libraries and, where configured, local machine-learning models.

The proposed system consists of two primary functional modules:

**Module A — Court Document Organizer**

Extracts and organizes information from an uploaded judgment.

**Module B — Similar Case Finder**

Compares the uploaded judgment with a prepared collection and retrieves potentially related judgments.

The modules share extracted text and structured case information.

**3.2 User Classes**

**3.2.1 Court Clerks**

May use the system to review document contents, identify important fields, and organize judgments.

**3.2.2 Junior Lawyers and Legal Researchers**

May use the application to identify legal issues, locate provisions, and discover documents worth further review.

**3.2.3 Law Students**

May use the system for educational exploration of legal judgments.

**3.2.4 General Citizens**

May use the structured summary to understand basic information in a judgment, subject to the limitations of automated extraction.

**3.2.5 Project Administrator**

The administrator is responsible for preparing the demonstration dataset, validating source records, and maintaining the local collection.

**3.3 Operating Environment**

The initial prototype targets:

- Operating system: Windows 10 or Windows 11.

- Programming language: Python 3.11 or another compatible version.

- User interface: Streamlit.

- PDF processing: PyMuPDF.

- Similarity search: Sentence Transformers and scikit-learn.

- Storage: JSON files or SQLite.

- Optional local LLM: Ollama with Qwen2.5 3B.

- Optional OCR: Tesseract.

- Optional charts: Plotly.

- Hardware: approximately 8 GB RAM, Intel Core i5 or comparable processor, and no dedicated GPU.

Exact library versions must be checked for compatibility during installation.

**3.4 Assumptions**

- The user can access the application through a supported web browser.

- The demonstration dataset is prepared before the demonstration.

- Most sample judgments are available as PDFs.

- The prototype initially processes English-language documents.

- The user has permission to process the selected documents.

- A local embedding model is downloaded before offline operation is required.

- OCR is needed only for scanned or image-based pages.

- Users will verify important extracted information against original judgments.

- The prepared dataset contains sufficient variation to demonstrate similarity retrieval.

**3.5 Constraints**

- The project must be implemented within approximately eight hours.

- The development computer has limited RAM and no dedicated GPU.

- The dataset is small and cannot represent all Indian legal matters.

- The embedding model is general-purpose rather than specifically trained for Indian law.

- Long documents may require chunking or summarization.

- Local language-model inference may be slow on a CPU.

- External legal websites may restrict automated downloads.

- OCR quality depends on scan resolution, page orientation, and document quality.

**3.6 Design Principles**

Proof Keeper shall follow these principles:

- **Evidence first:** Important extracted information should be traceable to source text.

- **No invented facts:** Missing information must be marked as unavailable or uncertain.

- **Transparent ranking:** The system should explain why a case was retrieved.

- **Human review:** Automated outputs are preliminary and must be verifiable.

- **Separation of facts and similarity:** Similarity must not be presented as proof of identical facts or outcomes.

- **Minimal complexity:** The MVP should prioritize reliable end-to-end functionality over advanced infrastructure.

**4. Functional Requirements**

Each requirement has a unique identifier and an acceptance criterion.

**4.1 Document Upload and Validation**

**FR-01: PDF Upload**

The system shall allow the user to upload a court judgment or order in PDF format.

**Acceptance criteria:**

- A valid PDF can be selected and submitted.

- The interface displays the selected filename.

- Unsupported file types are rejected with an understandable message.

**FR-02: File Validation**

The system shall validate the uploaded file before processing it.

**Acceptance criteria:**

- Invalid or unreadable PDFs are rejected.

- Empty files are rejected.

- Files exceeding the configured size limit are rejected with a message.

- The configured size limit is displayed or documented.

**FR-03: PDF Text Extraction**

The system shall extract text from readable PDF pages using PyMuPDF.

**Acceptance criteria:**

- Extracted text is available for subsequent analysis.

- Page boundaries are retained.

- The system detects when no meaningful text can be extracted.

**FR-04: Scanned PDF Detection**

The system should identify documents or pages that appear to contain images rather than extractable text.

**Acceptance criteria:**

- The user is informed when OCR may be required.

- The system does not silently present an empty extraction as a successful analysis.

**FR-05: OCR Processing — Optional**

If Tesseract is installed and enabled, the system may use OCR to extract text from scanned pages.

**Acceptance criteria:**

- OCR output is associated with the corresponding page.

- OCR failure is reported without crashing the entire application.

- The interface identifies OCR-derived text when practical.

**4.2 Case Information Extraction**

**FR-06: Case Category Identification**

The system shall identify the likely category of the judgment, including civil or criminal where supported.

**Acceptance criteria:**

- The displayed category is based on the extracted document.

- Uncertain classifications are marked as uncertain.

- The system does not force a civil/criminal label when the document cannot be classified reliably.

**FR-07: Party Extraction**

The system shall attempt to extract the names of parties and their roles, such as petitioner, respondent, appellant, or accused.

**Acceptance criteria:**

- Extracted names and roles are displayed in a structured format.

- Missing party information is marked as unavailable.

- Multiple parties can be represented.

**FR-08: Legal Act and Provision Extraction**

The system shall identify explicitly mentioned Acts, statutes, articles, rules, and sections where possible.

**Acceptance criteria:**

- Detected references are displayed as a list.

- The original text containing each reference is retained where available.

- The system does not invent provisions that are absent from the source text.

**FR-09: Legal Issue Extraction**

The system shall generate a concise description of the main legal issue or issues.

**Acceptance criteria:**

- The result is displayed separately from the case summary.

- The issue description is based on extracted document content.

- If reliable extraction is not possible, the system displays an uncertainty notice.

**FR-10: Key Facts Extraction**

The system shall identify a small number of important factual details relevant to understanding the case.

**Acceptance criteria:**

- The interface displays a concise list of extracted facts.

- Facts are not presented as verified independently of the judgment.

- Source passages are retained when feasible.

**FR-11: Outcome Extraction**

The system shall attempt to identify the final decision or disposition recorded in the document.

**Acceptance criteria:**

- The outcome is displayed separately from the legal issue and summary.

- The source passage supporting the outcome is retained where available.

- If the document is an interim order or the final disposition is unclear, the system states this rather than assuming a final outcome.

**FR-12: Case Summary**

The system shall provide a concise summary of the judgment.

**Acceptance criteria:**

- The summary is displayed in a readable format.

- It distinguishes the principal issue, relevant facts, and outcome where these are available.

- It does not knowingly introduce details unsupported by the extracted text.

**FR-13: Evidence and Page References**

The system shall preserve page references for extracted text and supporting passages.

**Acceptance criteria:**

- Page references are displayed where the source page is known.

- Supporting passages are taken from the extracted document text.

- The system does not fabricate a quotation or page number.

- If a reliable page reference is unavailable, the interface indicates that limitation.

**4.3 Similar Case Finder**

**FR-14: Preloaded Judgment Collection**

The system shall maintain a predefined collection of approximately 20–50 sample judgments for the prototype.

**Acceptance criteria:**

- The application can load the prepared collection.

- Each record has a unique identifier and source information.

- Missing or unreadable records are reported and skipped without stopping all processing.

**FR-15: Judgment Representation**

The system shall prepare a compact searchable representation of each judgment containing, where available:

- Legal issue.

- Key facts.

- Acts and provisions.

- Case category.

- Outcome.

- Source references.

**Acceptance criteria:**

- Each valid record has a searchable representation.

- Preprocessing is performed before the demonstration where practical.

- The uploaded judgment is converted to the same representation before comparison.

**FR-16: Semantic Similarity**

The system shall compare legal-issue representations using sentence embeddings.

**Acceptance criteria:**

- The same embedding model and compatible preprocessing are used for the query and stored cases.

- Semantic similarity is calculated for eligible records.

- Processing failures are reported and do not silently become valid scores.

**FR-17: Legal Provision Matching**

The system shall compare detected legal Acts and provisions between the uploaded judgment and stored judgments.

**Acceptance criteria:**

- Shared provisions contribute to the ranking.

- Provision names are normalized where practical.

- Missing provisions do not automatically cause a case to be excluded.

**FR-18: Fact and Keyword Matching**

The system shall compare relevant facts or legal terminology between judgments.

**Acceptance criteria:**

- A lexical similarity signal is calculated for eligible records.

- The signal is combined with other available signals.

- The system does not rely exclusively on case titles.

**FR-19: Similarity Ranking**

The system shall rank eligible judgments using a combined score.

**Acceptance criteria:**

- The highest-scoring eligible records appear first.

- The uploaded judgment itself is excluded from the results when it is already present in the collection.

- Up to five results are displayed, or fewer when fewer eligible records exist.

- Scores are identified as prototype similarity scores, not legal relevance probabilities.

**FR-20: Match Explanation**

The system shall explain why each retrieved judgment was selected.

**Acceptance criteria:**

- The result identifies available shared legal issues, provisions, or relevant terms.

- Explanations are based on calculated matching signals and extracted metadata.

- The interface does not claim that a case is legally applicable solely because its score is high.

**FR-21: Actual Outcome Display**

The system shall display the stored outcome of each retrieved judgment separately from its similarity explanation.

**Acceptance criteria:**

- The outcome comes from the stored record.

- Unknown outcomes are shown as unavailable.

- The interface does not infer that the uploaded case should receive the same outcome.

**FR-22: Source Access**

The system shall provide access to the original judgment PDF or recorded source URL where available.

**Acceptance criteria:**

- Each result identifies its source.

- Local files can be opened when supported by the interface.

- External URLs are displayed only when they are recorded and valid.

**4.4 User Interface**

**FR-23: Dashboard**

The application shall provide a simple interface containing:

- PDF upload.

- Processing status.

- Extracted case information.

- Case summary.

- Similar case results.

- Supporting evidence and source details.

**FR-24: Error Messages**

The application shall display actionable messages for common failures.

Examples include:

- Invalid PDF.

- No extractable text.

- OCR unavailable.

- Analysis failed.

- Dataset unavailable.

- No eligible similar cases found.

**FR-25: Uncertainty Indicators**

The interface shall identify fields that are missing or could not be extracted confidently.

The absence of a field must not be represented as proof that the information does not exist in the judgment.

**5. Non-Functional Requirements**

**5.1 Performance**

**NFR-01: Dataset Size**

The MVP shall support a prepared collection of 20–50 judgments.

**NFR-02: Retrieval Time**

For 20–50 preprocessed records, the ranking stage should ordinarily complete within five seconds on the target laptop, excluding PDF extraction and model initialization.

This is a target to verify during testing, not a guaranteed performance result.

**NFR-03: Processing Feedback**

The interface shall indicate that processing is in progress when a document is being analyzed.

**NFR-04: Resource Use**

The application should avoid unnecessary repeated embedding calculations and repeated processing of unchanged dataset records.

**5.2 Usability**

**NFR-05: Simplicity**

A first-time user should be able to upload a supported PDF and locate its extracted summary and similar cases without command-line interaction.

**NFR-06: Readability**

Results shall be organized using clear headings, labels, and readable text.

**NFR-07: Error Recovery**

An invalid document shall not terminate the application or prevent the user from attempting another upload.

**5.3 Reliability**

**NFR-08: Failure Isolation**

A single failed dataset record should not prevent the remaining valid records from being searched.

**NFR-09: Repeatability**

The same document processed with the same model, configuration, and dataset should produce substantially consistent rankings. Any nondeterministic LLM behavior should be documented.

**NFR-10: Graceful Degradation**

If the optional LLM or OCR component is unavailable, the application should retain core functionality wherever possible.

**5.4 Accuracy and Transparency**

**NFR-11: Source Traceability**

Important extracted fields should have supporting source text or an explicit indication that evidence is unavailable.

**NFR-12: Similarity Transparency**

The interface shall distinguish similarity scores from probabilities, legal conclusions, and binding precedent assessments.

**NFR-13: Evaluation**

The team shall manually evaluate the top-five results for at least five query judgments where a suitable labeled set is available.

Precision@5 shall be recorded as a prototype evaluation metric.

**5.5 Security and Privacy**

**NFR-14: Local Processing**

The preferred configuration shall process documents locally.

If an external service is added, the system must disclose what data is transmitted and obtain appropriate authorization.

**NFR-15: Temporary Files**

Temporary extracted text and intermediate files should be stored only as necessary and cleaned up when appropriate.

**NFR-16: Data Handling**

The application shall not claim that uploaded documents are permanently confidential unless the actual storage and deployment design supports that claim.

**NFR-17: Input Safety**

Uploaded files must be treated as untrusted input. The system should validate file type, size, and processing errors.

**5.6 Maintainability**

**NFR-18: Modular Design**

PDF extraction, information extraction, similarity ranking, storage, and UI code should be separated into distinct modules where practical.

**NFR-19: Configuration**

Dataset paths, result limits, and similarity weights should be configurable without extensive code changes.

**NFR-20: Portability**

The application should be runnable through documented Python environment and startup instructions.

**6. External Interface Requirements**

**6.1 User Interface**

The user interface shall be implemented using Streamlit.

Required screens or sections:

- **Upload section:** Upload and validate the judgment PDF.

- **Analysis section:** Display case category, parties, Acts, legal issues, facts, outcome, and summary.

- **Similar cases section:** Display ranked related judgments and match explanations.

- **Evidence section:** Show source passages, page references, and source links.

- **Status and error section:** Display progress, warnings, and processing failures.

A single-page interface is sufficient for the MVP.

**6.2 Software Interfaces**

| **Component** | **Technology** | **Purpose** |
| --- | --- | --- |
| Application | Python | Main processing logic |
| Frontend | Streamlit | Browser-based UI |
| PDF parser | PyMuPDF | Extract text and page information |
| OCR | Tesseract, optional | Extract text from scanned pages |
| Embedding model | Sentence Transformers | Generate semantic vectors |
| Initial embedding model | all-MiniLM-L6-v2 | General-purpose English sentence embeddings |
| Lexical similarity | scikit-learn | TF-IDF and cosine similarity |
| Local LLM | Ollama + Qwen2.5 3B, optional | Structured extraction and summaries |
| Storage | JSON or SQLite | Store case metadata and extracted information |
| Visualization | Plotly, optional | Charts and score comparisons |

**6.3 Hardware Interface**

No special hardware interface is required.

The application shall run on a normal laptop and should not require a dedicated GPU for the basic retrieval workflow.

**6.4 Network Interface**

The MVP shall not require continuous internet access after its required packages, models, and dataset have been prepared, provided all selected components operate locally.

Internet access may be required to download packages, models, or source documents before the demonstration.

**7. System Architecture and Design**

**7.1 High-Level Architecture**

The system shall follow this processing pipeline:

**User → Streamlit UI → PDF Text Extraction → Structured Information Extraction → Case Representation → Similarity Engine → Ranked Results → Evidence-Based Display**

The preloaded dataset follows a separate preprocessing pipeline:

**Sample Judgments → PDF Extraction → Metadata Preparation → Embeddings and Lexical Features → Local Dataset Storage**

When a new judgment is uploaded, the application generates a comparable representation and searches the prepared collection.

**7.2 Component Responsibilities**

**A. User Interface Module**

Responsibilities:

- Accept uploads.

- Display status and errors.

- Show extracted information.

- Present ranked cases and supporting evidence.

**B. Document Processing Module**

Responsibilities:

- Validate PDFs.

- Extract text page by page.

- Detect empty or image-based pages.

- Preserve page references.

- Invoke OCR if configured.

**C. Information Extraction Module**

Responsibilities:

- Identify parties and case category.

- Extract Acts and sections.

- Identify legal issues and key facts.

- Extract or summarize the outcome.

- Produce a concise case representation.

The MVP may use regular expressions and rule-based extraction for explicit patterns, with a local LLM added if time and hardware permit.

**D. Similarity Engine**

Responsibilities:

- Generate embeddings for legal-issue representations.

- Calculate semantic similarity.

- Compare provisions and relevant keywords.

- Combine available signals into a ranking.

- Return explanations derived from the matching signals.

**E. Storage Module**

Responsibilities:

- Store metadata.

- Store extracted summaries.

- Store source references.

- Store embeddings or preprocessed feature representations.

- Retrieve records for similarity search.

**F. Evidence Module**

Responsibilities:

- Preserve original text passages.

- Associate passages with source pages.

- Display evidence supporting extracted fields.

- Provide links to original source documents where available.

**7.3 Suggested Project Structure**

proof_keeper/

├── app.py

├── requirements.txt

├── README.md

├── config.py

├── modules/

│   ├── pdf_processor.py

│   ├── text_extractor.py

│   ├── information_extractor.py

│   ├── similarity_engine.py

│   ├── evidence_manager.py

│   └── storage.py

├── dataset/

│   ├── judgments/

│   └── cases.json

├── models/

│   └── README.txt

├── cache/

└── tests/

    ├── test_pdf_processing.py

    ├── test_extraction.py

    └── test_similarity.py

This is a recommended structure, not a requirement to create every file during the hackathon.

**8. Similar Case Finder Requirements and Algorithm**

**8.1 Objective**

The Similar Case Finder shall retrieve judgments that may discuss similar legal issues or facts.

The system is intended to support discovery, not determine legal authority or legal applicability.

**8.2 Inputs**

The system shall use available fields from the uploaded judgment:

- Legal-issue description.

- Key facts.

- Detected Acts and sections.

- Relevant text or keywords.

- Case category.

**8.3 Similarity Signals**

The initial prototype shall use three signals.

**Signal A: Semantic Similarity**

Sentence embeddings shall represent the legal-issue descriptions.

Cosine similarity shall be used to compare the uploaded judgment with each stored judgment.

**Signal B: Shared Legal Provisions**

The system shall compare normalized Acts and statutory provisions.

Exact shared provisions may contribute more strongly than a generic shared Act name.

**Signal C: Fact and Keyword Similarity**

The system shall compare relevant facts or text representations using TF-IDF and cosine similarity, or a simpler lexical overlap method if time is limited.

**8.4 Initial Ranking Formula**

The initial configurable formula shall be:

**Combined Score = 0.60 × Semantic Score + 0.25 × Legal Provision Score + 0.15 × Fact/Keyword Score**

All component scores shall be normalized to the range 0–1 before combination.

The weights are initial prototype settings, not empirically validated legal-relevance weights. The team may change them based on manual evaluation.

If a component is unavailable, the implementation should use a documented fallback, such as renormalizing the weights of available components. It must not silently treat missing data as a perfect match.

**8.5 Ranking Output**

Each result shall contain:

- Case identifier.

- Case name, where known.

- Court and date, where available.

- Overall similarity score.

- Matched legal issue.

- Shared Acts or provisions.

- Supporting passage and page reference.

- Actual outcome, if reliably extracted.

- Source URL or local PDF path.

**8.6 Ranking Limitations**

The system shall not:

- Treat the score as the probability of legal relevance.

- Claim that the retrieved judgment is binding precedent.

- Assume that a shared Act means the cases raise the same legal question.

- Infer that the same outcome should apply to the uploaded case.

- Hide the fact that the database contains only a small sample of judgments.

The general-purpose embedding model may miss important legal distinctions. Human review is therefore necessary.

**9. Data Requirements and Data Model**

**9.1 Data Sources**

The prototype dataset may contain judgments obtained manually from public legal sources, including official court portals and other sources that permit the intended use.

Each record should retain:

- Original source URL.

- Court name, where known.

- Case name or identifier.

- Judgment date, where known.

- Date downloaded or collected.

- Relevant use or redistribution restrictions, where applicable.

The project team must respect the source website's terms and applicable copyright rules. Public accessibility does not automatically mean unrestricted redistribution.

**9.2 Case Record**

A suggested JSON representation is:

{

  "case_id": "CASE_001",

  "case_name": "Verified case name",

  "court": "Court name",

  "judgment_date": "YYYY-MM-DD",

  "source_url": "https://example.org/source",

  "local_pdf_path": "dataset/judgments/case_001.pdf",

  "case_category": "Civil",

  "parties": [],

  "acts_and_sections": [],

  "legal_issues": [],

  "key_facts": [],

  "outcome": {

    "text": "",

    "source_page": null,

    "evidence_text": ""

  },

  "summary": "",

  "embedding": [],

  "metadata_verified": false

}

The example contains placeholder values, not a real judgment record.

**9.3 Data Validation**

The application shall validate required fields when loading the dataset.

- Every record shall have a unique identifier.

- Missing metadata shall be permitted where the source does not provide it.

- Invalid embeddings shall be regenerated or the record excluded from semantic ranking.

- A missing outcome shall be represented as unknown rather than inferred.

- Source provenance shall be retained whenever available.

**9.4 Dataset Size**

The initial target is 20–50 judgments.

The dataset is intended for demonstration and limited evaluation only. It is not a complete or representative legal database.

**10. Use Cases**

**UC-01: Upload and Analyze a Judgment**

**Actor:** User

**Preconditions:**

- The application is running.

- The user has a supported PDF.

**Main flow:**

- The user opens Proof Keeper.

- The user uploads a PDF.

- The system validates the file.

- The system extracts text and page information.

- The system extracts available case details.

- The system generates a summary.

- The system displays structured results and evidence.

**Alternative flows:**

- Invalid PDF: display an error and request another file.

- Empty text: recommend OCR or another document.

- Extraction failure: show a failure message and preserve application availability.

**Postcondition:** The user can review the extracted information and its limitations.

**UC-02: Find Similar Judgments**

**Actor:** User

**Preconditions:**

- A judgment has been processed.

- The prepared dataset is available.

**Main flow:**

- The system prepares a representation of the uploaded judgment.

- It compares the representation with eligible stored records.

- It calculates available similarity signals.

- It ranks the results.

- It displays the top five eligible judgments.

- It shows match explanations, outcomes, and source references.

**Alternative flows:**

- No dataset: display an actionable error.

- No eligible results: display an appropriate message.

- Missing metadata: rank using the remaining available signals and indicate limitations.

**Postcondition:** The user can inspect potentially related judgments.

**UC-03: Verify an Extracted Result**

**Actor:** User

**Preconditions:**

- A result contains a source passage or page reference.

**Main flow:**

- The user selects an extracted field or similar-case result.

- The system displays the supporting passage and page.

- The user compares the result with the original document.

- The user decides whether the information is suitable for further use.

**Postcondition:** The user can manually verify the extracted information.

**11. Error Handling**

The system shall handle common failures gracefully.

| **Error condition** | **Required behavior** |
| --- | --- |
| Invalid PDF | Reject the file and explain the problem |
| File too large | Display the configured size limit |
| PDF has no extractable text | Recommend OCR or a text-based PDF |
| OCR unavailable | Continue without OCR where possible and warn the user |
| Local LLM unavailable | Use the implemented fallback or disable LLM-dependent fields |
| Embedding model unavailable | Explain that semantic search cannot run |
| Dataset missing | Show a clear setup error |
| Invalid dataset record | Skip the record and report the issue |
| No similar cases | Display an empty-result message |
| Unknown outcome | Mark the outcome unavailable |
| Missing source page | Avoid inventing a page number |
| Processing timeout | Stop the failed operation safely and allow retry |

Errors shall not be represented as successful analyses.

**12. Security, Privacy, and Responsible Use**

**12.1 Local Processing**

The preferred implementation shall process uploaded documents locally.

No external LLM or cloud processing service should be used without an explicit design decision and appropriate user disclosure.

**12.2 Document Privacy**

Some legal documents may contain personal or sensitive information.

The prototype should:

- Avoid logging complete judgment contents unnecessarily.

- Avoid exposing temporary files through public web paths.

- Avoid storing uploaded documents longer than required.

- Explain where uploaded files are stored.

- Avoid claiming that the application provides professional-grade confidentiality without appropriate controls.

**12.3 Responsible AI**

The application shall:

- Display an informational disclaimer.

- Encourage verification against the original judgment.

- Indicate missing or uncertain information.

- Keep similarity and actual outcome separate.

- Avoid presenting automated outputs as legal advice.

- Avoid claiming that a retrieved case determines the outcome of another case.

**12.4 Legal and Research Disclaimer**

The interface shall display the following or equivalent wording:

“Proof Keeper is a prototype for document organization and legal research assistance. Its extracted information, summaries, and similarity results may contain errors or omissions. Similarity does not establish that a judgment is legally applicable or binding. Users should verify important information against the original court document and consult a qualified legal professional where appropriate.”

**12.5 Source Integrity**

The system shall preserve source references for dataset records whenever possible.

Source text should not be altered and then represented as a direct quotation. Generated summaries must be distinguishable from original judicial text.

**13. Testing Strategy**

**13.1 Testing Objectives**

Testing shall verify that:

- PDFs are accepted and processed correctly.

- Extracted information is presented in a usable format.

- Missing data is handled safely.

- Similarity ranking is repeatable.

- Match explanations correspond to available matching signals.

- Source evidence is traceable.

- The application can recover from common errors.

**13.2 Unit Testing**

Test the following components individually:

- PDF validation.

- Text extraction.

- Page-number preservation.

- Legal provision extraction.

- Embedding generation.

- Similarity calculation.

- Ranking order.

- Dataset loading.

- Error handling.

**13.3 Integration Testing**

Verify the end-to-end flow:

- Upload a judgment.

- Extract its text.

- Generate structured information.

- Compare against the prepared dataset.

- Display results with evidence.

**13.4 Test Cases**

| **Test ID** | **Scenario** | **Expected result** |
| --- | --- | --- |
| TC-01 | Upload a valid text-based PDF | Text is extracted |
| TC-02 | Upload a non-PDF file | File is rejected |
| TC-03 | Upload a PDF with no extractable text | Warning or OCR suggestion is displayed |
| TC-04 | Upload a judgment with named parties | Parties are extracted where identifiable |
| TC-05 | Upload a judgment containing statutory references | Detected provisions are displayed |
| TC-06 | Upload a judgment with an identifiable final order | Outcome and supporting passage are displayed |
| TC-07 | Search with a judgment similar to a stored case | Relevant stored case appears in the ranked results where the method supports the match |
| TC-08 | Search with a different legal issue | Ranking is calculated without assuming the same topic |
| TC-09 | Remove an optional outcome field from a record | The result displays outcome as unavailable |
| TC-10 | Remove one dataset record | Other valid records remain searchable |
| TC-11 | Run the same query twice | Rankings are substantially consistent under the same configuration |
| TC-12 | Inspect a displayed evidence passage | Passage corresponds to the recorded source text |
| TC-13 | Disable the optional LLM | Core retrieval continues if the fallback is implemented |
| TC-14 | Disable OCR | Text-based PDFs remain processable |
| TC-15 | Search with no valid dataset | A clear error is displayed |

**13.5 Retrieval Evaluation**

The team shall prepare a small manually labeled evaluation set.

Suggested procedure:

- Select five judgments as test queries.

- For each query, manually identify relevant cases from the available collection.

- Run the Similar Case Finder.

- Inspect the top five retrieved results.

- Record which results are relevant.

- Calculate Precision@5.

**Precision@5 = Number of relevant results among the top five / 5**

For example, if three of the five retrieved cases are manually judged relevant, Precision@5 is 0.60, or 60%.

This metric evaluates retrieval against the team's small labeled set. It does not establish legal correctness or general performance across Indian judgments.

**13.6 Manual Verification**

The team shall manually inspect:

- At least five query judgments.

- The displayed outcome of selected results.

- Source passages for key extracted fields.

- The explanations shown for top matches.

Any known errors discovered during testing should be documented.

**14. Risks and Mitigation**

| **Risk** | **Severity** | **Mitigation** |
| --- | --- | --- |
| Too few comparison judgments | High | Prepare 20–50 sample judgments in advance |
| Irrelevant similarity matches | High | Combine semantic, provision, and lexical signals |
| Incorrect extracted outcomes | High | Retain source evidence and require verification |
| Long-document processing failure | Medium | Process page by page and create compact representations |
| Model runs slowly on CPU | High | Precompute dataset features and keep LLM optional |
| Scanned PDFs cannot be read | Medium | Detect low-text pages and provide optional OCR |
| Embedding model misses legal nuance | High | Evaluate manually and disclose limitations |
| Dataset source or reuse restrictions | Medium | Record provenance and check applicable terms |
| Missing metadata | Medium | Allow unknown fields and use available signals |
| Hackathon time expires | High | Prioritize core upload, ranking, and evidence workflow |
| LLM invents details | High | Validate output, preserve evidence, and avoid unsupported claims |
| Model or package installation fails | Medium | Prepare the environment before the hackathon |

**15. Eight-Hour Implementation Plan**

This plan assumes development begins with a clean project but prioritizes a narrow, working prototype. Optional features may be dropped if time becomes limited.

**Hour 1 — Dataset and Environment**

Tasks:

- Set up Python environment.

- Install core dependencies.

- Prepare 20–30 sample judgments or a smaller usable subset.

- Create metadata records and source references.

Deliverable: A working environment and an initial dataset.

**Hour 2 — PDF Processing**

Tasks:

- Implement PDF upload.

- Validate file type and size.

- Extract text page by page.

- Detect empty or scanned documents.

Deliverable: Extracted text with page references.

**Hour 3 — Structured Analysis**

Tasks:

- Extract legal provisions using rules or patterns.

- Identify parties and case category where possible.

- Generate a concise legal-issue representation.

- Identify the outcome and supporting passage where possible.

Use the local LLM only if it can be installed and run reliably within the available time.

Deliverable: Structured case information.

**Hour 4 — Similarity Features**

Tasks:

- Load the embedding model.

- Generate embeddings for prepared legal-issue descriptions.

- Save the vectors.

- Implement lexical similarity.

Deliverable: A searchable set of preprocessed cases.

**Hour 5 — Ranking Engine**

Tasks:

- Compare the uploaded judgment with stored cases.

- Calculate semantic, provision, and lexical scores.

- Combine available scores.

- Return the top five results.

Deliverable: A working Similar Case Finder.

**Hour 6 — Evidence and Explanations**

Tasks:

- Display why each result matched.

- Show the actual stored outcome separately.

- Add source pages and supporting passages.

- Handle missing data.

Deliverable: Explainable ranked results.

**Hour 7 — Interface Integration**

Tasks:

- Complete the Streamlit interface.

- Connect upload, extraction, ranking, and evidence components.

- Add loading indicators and error messages.

Deliverable: An end-to-end working prototype.

**Hour 8 — Testing and Demonstration**

Tasks:

- Test at least five query judgments where feasible.

- Inspect top results.

- Correct major extraction or ranking issues.

- Prepare a short demonstration and explain the limitations.

Deliverable: A demonstrable MVP with documented evaluation.

**Time-management rule:** A working upload-to-results flow is more valuable than a sophisticated model that has not been integrated or tested.

**16. Acceptance Criteria**

The project shall be considered a successful MVP when the following conditions are met:

- The application launches on the target Windows environment.

- A supported judgment PDF can be uploaded.

- Text can be extracted from ordinary text-based PDFs.

- The system displays a structured summary and available case information.

- Missing or uncertain fields are handled without inventing facts.

- The prepared judgment collection can be loaded.

- The Similar Case Finder ranks eligible judgments.

- The top five results are shown when five eligible records exist.

- Results explain their available similarity signals.

- Original source passages and page references are shown where available.

- Actual outcomes are displayed separately from similarity scores.

- The application handles common processing failures gracefully.

- At least five query judgments are manually evaluated where a suitable labeled set exists.

- The project demonstrates its limitations and retains human verification.

- The prototype does not claim to provide binding legal conclusions.

Optional OCR, charts, downloadable reports, and LLM-assisted extraction are not mandatory acceptance criteria.

**17. Future Enhancements**

Potential future improvements include:

- A larger, curated judgment database.

- Better models trained or evaluated specifically on Indian legal texts.

- Reranking with a cross-encoder or other more advanced retrieval model.

- Improved legal citation extraction and normalization.

- Support for additional Indian languages.

- More robust OCR for scanned documents.

- Search filters by court, date, jurisdiction, statute, and case category.

- Better handling of interim orders and procedural decisions.

- User feedback for correcting extracted fields.

- A persistent database and controlled dataset-management interface.

- Advanced citation analysis and relationship mapping.

- Evaluation against a larger manually annotated benchmark.

- User authentication and access controls for multi-user deployment.

- Improved document retention and privacy controls.

- More sophisticated source attribution and evidence navigation.

These enhancements should be implemented only after the core workflow has been tested.

**18. Demo Scenario**

The demonstration shall use a prepared judgment and a curated set of related sample judgments.

**Step 1: Upload**

The user uploads a sample property-dispute judgment.

**Step 2: Extract**

Proof Keeper extracts text and displays:

- Case category.

- Parties.

- Acts and sections.

- Legal issue.

- Key facts.

- Summary.

- Outcome, if identified reliably.

**Step 3: Review Evidence**

The user opens a supporting passage and checks the associated source page.

**Step 4: Find Similar Cases**

The system compares the uploaded judgment with the prepared collection and returns the top five potentially related judgments.

**Step 5: Explain Matches**

For each result, the system shows:

- Similar legal issue.

- Shared provisions.

- Relevant matching terms or facts.

- Similarity score.

- Actual outcome from the stored judgment.

- Source reference and evidence.

**Step 6: Explain Limitations**

The presenter explains that the matches are research leads, not legal conclusions, and that the dataset is a prototype collection.

The demonstration should use genuine source judgments and verified metadata. Any illustrative data must be labeled clearly.

**19. Conclusion**

Proof Keeper is designed as a practical legal-document organization and discovery prototype. It combines PDF text extraction, structured case information, semantic similarity, legal provision matching, and evidence-based presentation.

The central goal is to reduce the initial effort required to understand a lengthy judgment and identify other documents worth reviewing.

The project deliberately limits its initial scope to a small, prepared dataset and a lightweight local architecture suitable for an eight-hour hackathon. Its outputs are intended to assist human review rather than replace professional legal research or judicial decision-making.

The success of the MVP will be measured by its ability to complete the upload-to-analysis-to-similar-cases workflow, explain retrieved results, preserve source evidence, and handle uncertainty responsibly.

**Appendix A — Recommended Dependencies**

A minimal initial dependency list is:

streamlit

pymupdf

sentence-transformers

scikit-learn

numpy

pandas

Optional dependencies:

ollama

plotly

Tesseract OCR must be installed separately if OCR is enabled. The required language model must also be downloaded before local inference.

The exact package versions should be pinned after the application has been tested in the target environment.

**Appendix B — Final Scope Priority**

| **Priority** | **Requirement** |
| --- | --- |
| P0 — Essential | PDF upload and validation |
| P0 — Essential | Text extraction with page tracking |
| P0 — Essential | Structured legal information display |
| P0 — Essential | Preloaded sample judgment collection |
| P0 — Essential | Similarity ranking |
| P0 — Essential | Match explanation and source evidence |
| P0 — Essential | Actual outcome displayed separately |
| P0 — Essential | Basic errors and uncertainty handling |
| P1 — Optional | OCR for scanned PDFs |
| P1 — Optional | Local LLM for structured extraction |
| P1 — Optional | Search filters and interactive charts |
| P2 — Future | Larger datasets, legal-specific reranking, multilingual support, and production security |

**End of Document**