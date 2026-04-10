# Workbook UI Case Summary

## tc1
Uploads lab-report style documents. In UI terms, this checks the patient upload flow for PDF and text-like report content.

## tc2
Uploads medical-image style files. In UI terms, this checks the patient upload flow for image formats.

## tc3
Uploads audio files. In UI terms, this checks the patient upload flow for supported audio uploads.

## tc4
Covers the user-visible path before PDF extraction/processing. In UI this is mainly the upload plus doctor-side analyze action.

## tc5
Covers the user-visible path before TXT extraction/processing. In UI this is upload plus analyze for plain-text content.

## tc6
Covers the user-visible OCR path for an image upload and doctor-side analyze action.

## tc7
Covers the visible flow for MP3 upload followed by analyze, representing transcription before downstream processing.

## tc8
Covers the visible flow for WAV upload followed by analyze.

## tc9
Covers the failure path where audio analysis/transcription does not succeed.

## tc10
Covers the visible doctor question flow after upload, representing secure embedding-backed usage from the UI.

## tc11
Covers authorized doctor interaction with the assistant after approved access is in place.

## tc12
Covers the visible search/chat experience after files are available and processed.

## tc13
Covers an English natural-language question entered in the doctor assistant UI.

## tc14
Covers an English medical-abbreviation question in the doctor assistant UI.

## tc15
Covers the visible error path for a non-English question in the doctor assistant UI.

## tc16
Covers the doctor-side retrieval/chat experience for a relevant query.

## tc17
Covers multi-source retrieval from more than one uploaded document through the chat UI.

## tc18
Covers the low-relevance or no-good-match query path in the doctor assistant UI.

## tc19
Covers a unified answer from multiple uploaded sources in the doctor assistant UI.

## tc20
Covers a concise, non-redundant answer in the doctor assistant UI.

## tc21
Covers a source-grounded answer with confidence/source presentation in the UI.

## tc22
Covers PDF/text upload and analyze from the user’s visible workflow.

## tc23
Covers image upload and analyze from the user’s visible workflow.

## tc24
Covers audio upload and analyze from the user’s visible workflow.

## tc25
Covers single-source citation/source-chip display in the doctor chat UI.

## tc26
Covers multi-source citation/source-chip display in the doctor chat UI.

## tc27
Covers source link visibility/availability in the doctor chat UI.

## tc28
Covers the visible upload path while ensuring raw patient-name style identifiers do not surface in UI content.

## tc29
Covers the visible upload path while ensuring date-of-birth style identifiers do not surface in UI content.

## tc30
Covers the processed-file UI path where raw identifiers should not be shown back to users.

## tc31
Covers the approved doctor’s visible ability to access an assigned patient workspace/file relationship.

## tc32
Covers the unauthorized doctor visible path where the patient should not appear as accessible.

## tc33
Covers hidden/absent patient visibility for an unauthorized doctor.

## tc34
Covers the user-visible upload flow related to privacy expectations around patient-name masking.

## tc35
Covers the user-visible privacy expectation around DOB masking.

## tc36
Covers the user-visible privacy expectation around not exposing patient details during retrieval-related usage.

## tc37
Covers the visible revoke/disposal-style flow after authorization is no longer active.

## tc38
Covers the visible retained-access flow while authorization is still active.

## tc39
Covers immediate revoke from the patient UI.

## tc40
Covers registration through the UI.

## tc41
Covers password-update driven login success afterward.

## tc42
Covers the user login flow while ensuring the auth path works without exposing plaintext credentials in the visible experience.

## tc43
Covers the confirmation behavior after a successful upload.

## tc44
Covers the visible file/details state after a successful update-oriented workflow.

## tc45
Covers repeated successful upload/confirmation behavior.

## tc46
Covers text-plus-audio multi-modal visible workflow.

## tc47
Covers image-plus-document multi-modal visible workflow.

## tc48
Covers end-to-end multi-modal visible workflow across document, audio, and image content.
