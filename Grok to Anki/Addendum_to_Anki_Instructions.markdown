# Addendum to Anki Instructions

This addendum supplements the rules in `anki-instructions.txt` for creating Anki-compatible study questions for any subject area. Version 22 (October 1, 2025) consolidates to 34 statements from 33 in Version 21, incorporating detailed guidelines for structuring overlapping cloze deletions to balance enumeration complexity with atomicity through contextual cues and unified recall chunks, and adding specific tagging for overlapping clozes. The update ensures compatibility with spaced-repetition principles like minimizing cognitive load and enhancing ordered memorization.

1. **Focus on Core Certification-Relevant Concepts:** Generate questions only for explicitly stated concepts in the source text, prioritizing those tied to the target certification (e.g., CySA+ for cybersecurity). Exclude course-specific terms (e.g., course names, tools), pedagogical goals (e.g., learning objectives, course structure), or future learning statements (e.g., “In this module, you will…”), including such terms only in metadata or explanations unless they are general subject concepts.

2. **Structured Formatting for Questions:** Name CSV files by section (e.g., SA-X-X-X.csv, CD-X-X-X.csv, MCQ-X-X-X.csv), including only questions tagged with the relevant section (e.g., Section::X.X.X). Ensure tags include Section::X.X.X, topic, and question type (e.g., cloze, multiple-choice). For MCQ questions, include “multiple-correct” in tags for multi-correct questions and place Tags as the last CSV field. Verify all CSV fields (e.g., Front, Back, Text, Corrects, Distractors) are properly escaped for commas, pipes, and HTML tags to ensure Anki import compatibility.

3. **Cross-Check for Redundancy and Interference:** Compare proposed questions against existing ones in the same format (e.g., SA to SA, CD to CD, MCQ to MCQ) and broaden the check to include overlapping concepts or enumerations in prior conversations to ensure distinctness. Cross-check for interference to prevent confusingly similar questions.

4. **MCQ Format Specifications:** Generate all Multiple Choice questions in the MCQ - Multi-Variant Shuffled note type, ensuring `Question` and `QuestionPlural` fields are identical except for plurality (e.g., “Which is…” vs. “Which are…”), as `Question` appears on Choose-1 cards. Exclude hidden QID spans from both fields. For single-correct MCQs, set HasTwoCorrects and HasThreeCorrects to empty to suppress multi-correct cards. Ensure at least four distractors for full compatibility.

5. **Consistent MCQ Distractors:** For MCQ questions, ensure distractors match the form (single-word or phrase-length) and number (singular, plural, collective) of correct options, using varied, subject-relevant, and plausible distractors (e.g., related concepts, different categories/types, or processes) that avoid synonyms, overlap with existing distractors, additional examples of the concept (e.g., for security controls like Managerial, use Compliance, not Physical), or patterns that cue answers. Use full terms instead of initialisms to avoid cuing answers. Ensure distractors are clearly distinct from correct answers, avoiding options that are too closely related (e.g., secondary motivations like “Disruption/chaos” for hacktivists, or closely related defense methodologies like “Variety” for Defense in depth) to minimize interference, unless explicitly included as a correct answer with a clear explanation.

6. **Context Cues and Clarity:** Include a certification-specific context marker (e.g., “[CySA]”) in CD Text and SA/MCQ Front/Question fields to prime recall, avoiding extraneous phrases. Specify the intended focus in questions to avoid ambiguity (e.g., clarify scope or aspect), using context cues like “senior executive” for high-level roles to balance recall challenge. Ensure clean text and proper CSV field escaping.

7. **Handle Missing Source Details:** For topics not explicitly detailed in the source text, use standard worldview definitions or principles to derive atomic, explicit questions aligned with learning outcomes or key terms.

8. **Emphasize Accessibility:** Shape answers to highlight accessibility for relevant concepts (e.g., ease of use for tools) to reinforce significance without adding complexity.

9. **Reinforce Key Differentiations Across Formats:** Create Simple Answer (SA) questions for active recall of single concept definitions, Cloze Deletion (CD) for terms or phrases in enumerative lists, and Multiple Choice (MCQ) for scenario-based recognition. For fixed lists, MCQs may include multiple examples in multi-correct questions with distractors from distinct concepts. For open-ended enumerations (e.g., “including…”), use single- or multi-correct MCQs for recognition, ensuring distractors are not additional examples of the concept. Avoid SA questions for open-ended enumerations to prevent ambiguity. Reject sets overlapping too closely with existing questions.

10. **Track and Report Progress:** Maintain a running count of accepted questions per format (SA, CD, MCQ) and estimate total questions needed (e.g., 20 SA, 8-10 CD, 7-8 MCQ) based on source text complexity.

11. **Cloze Specificity and Completeness:** For Cloze Deletion (CD) questions, ensure each cloze targets a single, atomic fact with part-of-speech hints (e.g., `::action`, `::noun`) to clarify the expected answer type. For enumerative lists, include a note in the Extra field to clarify whether the list is exhaustive per the source text to prevent confusion about additional elements.

12. **Handle Enumerative Lists:** For fixed or ordered enumerative lists of four or fewer items, create CD questions with overlapping pairs (e.g., items 1-2, 2-3, 3-4) using identical cloze tags (e.g., `c1`) to obscure elements simultaneously, with prompts (e.g., one element or question cue) for ordered memorization. For longer lists, break into subsets (e.g., three clozes for five or more items). Ensure each overlapping cloze card provides contextual cues by including at least one enumerated item before the first cloze tag to indicate the starting position in the sequence; where possible, include at least one item after the last cloze tag to show continuation or completion, reducing ambiguity and aiding ordered memorization (e.g., for a list A, B, C, D: first card as 'List includes {{c1::A::item}}, {{c1::B::item}}, {{c1::C::item}}, D.'; middle card as 'List includes A, {{c1::B::item}}, {{c1::C::item}}, D.'; last card as 'List includes A, B, {{c1::C::item}}, {{c1::D::item}}.'). For open-ended enumerations (e.g., “including…”), prefer scenario-based SA or single- or multi-correct MCQ questions for recognition of one or more items, ensuring distractors are not additional examples of the concept.

13. **Multi-Cloze for Semi-Related or Non-Ordered Concepts:** For CD questions testing semi-related concepts (e.g., term and characteristic) or short unordered enumerations (up to three elements), use multiple clozes with different numbered tags (e.g., `c1`, `c2`) to obscure elements separately, equivalent to single-cloze instances or extending SA definitional relationships. Justify in metadata and use part-of-speech hints.

14. **Use Mnemonics for Complex Sequences:** For complex sequences or lists, incorporate mnemonic aids (e.g., acronyms, imagery) in 1–5% of questions, ensuring simplicity and relevance to the subject.

15. **Plausible Distractors from Non-Target Concepts:** For MCQ questions, select distractors from non-target entities or motivations within the same domain (e.g., for nation-state motivations, use hacktivist motives), ensuring plausibility without overlap with correct answers in other questions.

16. **Use Reverse Questions for Key Concepts:** For critical concepts, create forward (e.g., “What is X?”) and reverse (e.g., “What term describes Y?”) SA questions to reinforce bidirectional recall, ensuring distinct phrasing to avoid cuing.

17. **Prioritize High-Impact Concepts:** Focus questions on core definitions and critical processes, omitting minor details unless they enhance understanding of key principles.

18. **Incorporate Visual Cues When Applicable:** For subjects with visual components (e.g., networking), include text-based questions evoking imagery or flag for image occlusion in metadata (e.g., “Flag: Requires network topology image”), without generating images unless requested.

19. **Ensure Question Independence:** Each question should stand alone, except for assumed knowledge from prior sections per the source text’s structure.

20. **Balance Question Types:** Aim for a balanced distribution of SA (50%), CD (30%), and MCQ (20%) questions based on source text complexity, adjusting to cover all key concepts.

21. **Keep Scenarios Concise and Relevant:** In scenario-based questions, focus on a single concept or action with vivid, realistic examples (e.g., “An attacker scans a network”) to avoid cognitive overload.

22. **Use Standard Terminology:** Use standard subject-specific terms (e.g., “TCP” in networking, “white hat hacker” in cybersecurity) unless the source text specifies otherwise, testing terms distinctly with appropriate distractors.

23. **Simplify Complex Answers:** Break answers with multiple components (e.g., lists, multi-part definitions) into multiple SA or CD questions to ensure each targets a single, atomic fact.

24. **Use Active Voice in Questions:** Prefer active voice (e.g., “What does an attacker do to exploit X?”) for engagement and clarity, avoiding passive constructions unless required.

25. **Align with Certification Objectives:** Ensure questions align with the target certification’s objectives, focusing on emphasized knowledge and skills.

26. **Avoid Circular Question-Answer Pairs:** Ensure SA and CD questions elicit distinct aspects of a concept, not restating the answer (e.g., ask “Why does X principle avoid Y?” for rationale).

27. **Ensure Metadata Completeness:** Include detailed metadata in all questions, specifying question type (e.g., single-correct, multiple-cloze), rationale, and source reference (e.g., Section::X.X.X) for traceability.

28. **Avoid Ambiguous Phrasing:** Use precise phrasing (e.g., specify “in the context of X”) to prevent misinterpretation, especially for similar terms or applications.

29. **Leverage Source Text Structure:** Organize questions to follow the source text’s structure for incremental learning.

30. **Handle Sequential Processes in CD:** For processes with multiple sequential or related actions (e.g., vulnerability management), use CD questions with distinct numbered clozes (e.g., `c1`, `c2`, `c3`) and part-of-speech hints to cover all key actions atomically.

31. **Use MCQ for All Multiple Choice Questions:** Generate all Multiple Choice questions in the MCQ - Multi-Variant Shuffled note type, ensuring at least four distractors. For multi-correct MCQs, allow one or more correct answers as appropriate to the concept, without artificially inflating the number of correct answers.

32. **MCQ Explanation Format:** In MCQ questions, structure the `Explanation` field to provide individual explanations for each correct answer in the order of the `Corrects` field, separated by double pipes (`||`), followed by a single double pipe separator (`||`), then individual explanations for each distractor in the order of the `Distractors` field, also separated by double pipes (`||`). Ensure explanations are robust, avoid circular reasoning, detail why each option is correct or incorrect, and match the total number of explanations to the total number of options (corrects + distractors) to prevent mismatches during randomization by the MCQ - Multi-Variant Shuffled note type script. Use a single `||` separator between correct and distractor explanations to avoid rendering issues in Anki, as multiple consecutive pipes (e.g., `|| ||`) may cause formatting errors.

33. **Detailed MCQ Field Population and Conversion Guidelines:** When generating or converting MCQ questions to the "MCQ - Multi-Variant Shuffled" note type, populate fields as follows to support Choose-1, Choose-2, and Choose-3 card types with daily randomization:  
   - **Question**: Purpose: Prompt for Choose-1 card (single correct). Content: Clear, concise, singular question (e.g., "[CySA] Which is a programming language?"). Format: Plain text, avoid "||". Example: "[CySA] Which is a programming language?"  
   - **QuestionPlural**: Purpose: Prompt for Choose-2/Choose-3 cards (multiple corrects). Content: Plural adaptation (e.g., "[CySA] Which are programming languages?"). Format: Plain text, avoid "||". Example: "[CySA] Which are programming languages?"  
   - **Corrects**: Purpose: All possible correct answers. Content: At least 3 for full compatibility. Format: "||" separated, no trailing/leading "||", trim whitespace. Example: "Python||Java||C++||Ruby". Note: Fewer than 3 suppresses Choose-2/Choose-3 via marker fields.  
   - **Distractors**: Purpose: Incorrect options to mix in. Content: At least 4 for full compatibility, plausible but wrong. Format: "||" separated, no trailing/leading "||", trim whitespace. Example: "HTML||CSS||XML||JSON". Note: Fewer than 4 may show errors if not suppressed.  
   - **Explanation**: Purpose: Back-side explanations for all options, corrects highlighted green. Content: Explanations for each correct answer in `Corrects` order, separated by "||", followed by a single double pipe separator ("||"), then explanations for each distractor in `Distractors` order, separated by "||", clarifying correctness. Format: "||" separated, plain text or simple HTML. Example: "Python is a high-level, object-oriented, interpreted language.||Java is a compiled, object-oriented language.||C++ is the object-oriented successor of C.||HTML is a markup language for document formatting.||CSS is a style-sheet language for web styling." Note: Match total items to avoid mismatches, include single double pipe separator between correct and distractor explanations, and provide individual explanations for each distractor to prevent randomization issues.  
   - **Metadata**: Purpose: Differentiator for randomization. Content: Topic/label (e.g., “Test1”). Format: Plain text, avoid "||". Example: "Test1".  
   - **HasTwoCorrects**: Purpose: Enables Choose-2. Content: “true” if ≥2 corrects, else empty. Format: Plain text or empty.  
   - **HasThreeCorrects**: Purpose: Enables Choose-3. Content: “true” if ≥3 corrects, else empty. Format: Plain text or empty.  
   For conversions: Extract singular/plural questions; split options into Corrects/Distractors; provide ordered explanations with single double pipe separator between corrects and distractors; use topic for Metadata; set markers by correct count. Validate: ≥3 corrects/≥4 distractors preferred; match Explanation count; suppress via markers; avoid stray "||"; preview in Anki. For testing: Preview cards; verify suppression/highlighting/randomization; check for errors/mismatches.

34. **Tagging for Overlapping Clozes:** Use the tag 'overlapping-cloze' for cloze deletion questions involving overlapping enumerations, in place of or in addition to 'cloze', to distinguish them from single or independent clozes and facilitate targeted review or filtering in Anki decks.