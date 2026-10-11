# Test and Evaluation Sheet (owner: Sharvaree)

## A. Functional test cases
| ID | Test | Expected result | Pass/Fail | Notes |
| --- | --- | --- | --- | --- |
| T1 | Upload a normal text PDF | Text extracted, page numbers kept | | |
| T2 | Upload a .txt or .jpg file | Clear "unsupported file" message | | |
| T3 | Upload an empty file | Rejected with message | | |
| T4 | Upload a corrupted PDF | Error message, app does not crash | | |
| T5 | Upload a file above size limit | Rejected with size message | | |
| T6 | Upload a scanned PDF | "OCR may be required" warning, no fake success | | |
| T7 | Judgment with no Acts mentioned | Acts shows "Not found", nothing invented | | |
| T8 | Interim order | Outcome says final outcome unclear | | |
| T9 | Upload a case already in dataset | It is excluded from its own results | | |
| T10 | Delete cases.json temporarily | "Dataset unavailable" message | | |
| T11 | Run twice on same file | Same ranking both times | | |
| T12 | Turn off Wi-Fi after setup | App still works (local processing) | | |

## B. Precision@5 (SRS NFR-13: at least 5 query judgments)
Precision@5 = (number of relevant results in top 5) / 5.
A result is "relevant" if it is about a similar legal issue (judged by a teammate who read both).

| Query case | Top-5 case IDs | Relevant count (0-5) | Precision@5 | Comment |
| --- | --- | --- | --- | --- |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
| | | | | |
Average Precision@5: ______

## C. Manual verification of extraction (5 judgments)
| Case | Category correct? | Parties correct? | Acts/sections correct? | Outcome correct? | Page refs correct? |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

## D. Weight tuning log (optional)
| Semantic | Provision | Keyword | Avg Precision@5 |
| --- | --- | --- | --- |
| 0.60 | 0.25 | 0.15 | |
