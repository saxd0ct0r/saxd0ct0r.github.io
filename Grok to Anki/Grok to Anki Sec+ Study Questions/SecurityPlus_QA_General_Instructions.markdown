# General Project Instructions for CompTIA Security+ Q/A Pairs

## Objective
Generate and refine question-and-answer (Q/A) pairs for the CompTIA Security+ (SY0-701) exam, based on *Security Pro 8.0* materials, to prepare learners effectively while adhering to the *20 Rules of Formulating Knowledge* for optimal learning and retention. The Q/A pairs must cover key concepts, terms, and exam objectives, ensuring clarity, specificity, and active recall. Outputs will be delivered in markdown format for the Q/A list and, when requested, in CSV format for Anki import with `{{front}}` (question) and `{{back}}` (answer) fields. The instructions are designed to be applicable to any chapter or section of the *Security Pro 8.0* curriculum and can leverage prior Q/A sets uploaded in new conversations to maintain consistency and avoid redundancy.

## Content Requirements
1. **Source Material**:
   - Use content from specified *Security Pro 8.0* chapters or sections, prioritizing the most recent material provided when overlapping topics arise.
   - Cover all learning outcomes, key terms, and SY0-701 objectives (e.g., 1.1: security controls, 2.1: threats) as outlined in the source material.
   - Include topics such as:
     - Fundamental security concepts (e.g., CIA triad, non-repudiation).
     - Security controls (categories: Technical, Managerial, Operational, Physical; types: Preventive, Detective, Corrective, Deterrent, Directive, Compensating).
     - Threat actors and motivations (e.g., nation-state, organized crime, insider threats).
     - Risk management processes and roles.
     - Organizational security roles (e.g., CIO, CSO, ISSO, nontechnical staff).
     - Security policies and frameworks (e.g., NIST 800-53).
     - Countermeasures and incident response strategies.

2. **Coverage**:
   - Address all learning outcomes and key terms from the provided material without redundancy.
   - Consolidate overlapping content from prior Q/A sets (when uploaded) by prioritizing newer material and retaining non-overlapping items.
   - Ensure alignment with SY0-701 objectives, mapping questions to relevant domains (e.g., 1.1 for controls/roles, 2.1 for threats).

## Question and Answer Design
1. **General Guidelines**:
   - **Clarity (Rule 3)**: Use precise, unambiguous language in questions and answers to ensure immediate comprehension.
   - **Specificity (Rule 5)**: Craft questions with a single correct answer, avoiding vague or abstract terms (e.g., “describes,” “creates”).
   - **Simplicity (Rule 4)**: Keep answers minimal, focusing on one concept per question, avoiding extraneous details.
   - **Active Recall (Rule 8)**: Design questions to prompt direct retrieval of key facts or concepts, encouraging memorization through testing.
   - **Avoid Enumerations (Rule 10)**: Minimize list-based answers; if unavoidable, include clear numerical cues (e.g., “three types,” “four categories”) and consider splitting into sequential questions.
   - **Avoid Interference (Rule 11)**: Prevent overlap or redundancy between questions to avoid confusion and ensure distinct learning points.
   - **Context (Rule 6)**: Incorporate scenario-based questions where appropriate to reflect practical application, especially for SY0-701 objectives requiring examples.

2. **Question Structure**:
   - **Avoid One-to-Many Questions**: Do not ask for an example of a control, measure, or concept (e.g., “What is an example of a preventive control?”) as this allows multiple correct answers. Instead, specify the control or concept and ask for its type, category, purpose, or role (e.g., “What type of functional control is an ACL? A: Preventive”).
   - **Context-Independence**: Ensure each question is understandable in isolation, avoiding reliance on prior questions (e.g., avoid “another task” unless the context is explicit within the question).
   - **Concrete Phrasing**: Use direct, specific terms (e.g., “What type of control…,” “How quickly…,” “What role…”) instead of abstract terms (e.g., “describes,” “creates”).
   - **Cues for Enumerations**: For answers with multiple parts (e.g., three threats, four categories), include numerical cues in the question (e.g., “What are the three…”).
   - **Sequential Questions**: For processes (e.g., risk management steps), split enumerations into sequential questions with clear cues (e.g., “first step,” “second step”) to aid learning the order.

3. **Answer Design**:
   - **Minimal Information**: Provide concise, single-concept answers (e.g., “Preventive,” “Financial profit”) to avoid cognitive overload.
   - **Example-Free Unless Necessary**: Avoid examples in answers unless required for SY0-701 objectives (e.g., identifying a control’s category) or scenario-based questions. When included, use minimal, exam-relevant examples (e.g., “firewalls” for Technical controls).
   - **Single-Concept Focus**: Split complex or multi-part answers (e.g., multiple actions or conditions) into separate questions to ensure each focuses on one concept.

4. **Feedback Integration**:
   - **Splitting Multi-Part Answers**: Divide complex answers into multiple questions, each addressing a single concept (e.g., split a question about information security into separate questions for data, infrastructure, and threats).
   - **Context-Independence**: Ensure questions are standalone, avoiding phrases like “another” that imply prior context.
   - **Avoiding One-to-Many Questions**: Refactor questions asking for examples into ones specifying the item and asking for its classification or purpose.
   - **Concrete Phrasing**: Replace vague or abstract terms with specific, action-oriented phrasing (e.g., “How many…” instead of “What describes…”).
   - **Enumerations**: Split list-based answers into sequential questions or use clear numerical cues to facilitate learning.
   - **Prioritizing New Material**: When new material overlaps with prior content, prioritize the latest content and retain only non-overlapping prior questions.

## Output Requirements
1. **Markdown Format**:
   - Present Q/A pairs in markdown with numbered headings (e.g., `## Q1`, `## Q2`).
   - Include a brief *20 Rules* explanation for each question (e.g., `*Rule Applied*: Minimal information, focusing on one aspect for active recall”).
   - Use a consistent `artifact_id` for updates to the Q/A list, with a new `artifact_version_id` for each revision.
   - Title: `SecurityPlus_QA.md`, contentType: `text/markdown`.

2. **CSV for Anki**:
   - When requested, generate a CSV with two columns: `{{front}}` (question), `{{back}}` (answer).
   - Use quoted strings to handle commas in text (e.g., “Integrity ensures data accuracy; non-repudiation…”).
   - Include a header row (`{{front}},{{back}}`) and no additional fields (e.g., tags) unless specified.
   - Assign a new `artifact_id` for the CSV, title: `SecurityPlus_Anki_QA.csv`, contentType: `text/csv`.

3. **Artifact Handling**:
   - Wrap all outputs in `<xaiArtifact>` tags with attributes: `artifact_id`, `title`, `contentType`.
   - For Q/A list updates, reuse the existing `artifact_id` and increment `artifact_version_id`.
   - For new outputs (e.g., CSV, instructions), assign a new `artifact_id` in UUID format.
   - Never mention `<xaiArtifact>` tags or attributes outside the tag itself.

## Revision Process
1. **Analyze Feedback**:
   - Review user comments for specific issues (e.g., ambiguity, enumerations, one-to-many questions, vague phrasing).
   - Address identified issues by revising questions for specificity, splitting complex answers, or adding cues for enumerations.

2. **Incorporate New Content**:
   - Add questions for new chapters/sections, ensuring coverage of all learning outcomes and key terms.
   - Check for overlaps with prior Q/A sets (when uploaded) and consolidate by prioritizing newer material.

3. **Refactor for Clarity**:
   - Revise questions with ambiguous, abstract, or one-to-many phrasing to ensure a single correct answer.
   - Ensure context-independence by avoiding reliance on prior questions.
   - Split multi-part answers into separate, single-concept questions to reduce complexity.

4. **Maintain Exam Alignment**:
   - Map questions to SY0-701 objectives, ensuring coverage of relevant domains (e.g., 1.1: controls/roles, 2.1: threats).
   - Include scenario-based questions for practical application where required by exam objectives.

5. **Leverage Prior Q/A Sets**:
   - When a prior Q/A markdown is uploaded, use it to identify existing coverage and avoid redundancy.
   - Retain non-overlapping questions from prior sets and integrate new questions seamlessly, ensuring consistency in style and format.

## Continuous Improvement
- **Feedback-Driven Refinement**: Continuously incorporate user feedback to address issues like ambiguity, complex answers, or lack of context-independence.
- **Proactive Examination**: Regularly check for enumerations, one-to-many questions, or vague phrasing, refactoring as needed to maintain *20 Rules* compliance.
- **Scalability**: Design questions to be adaptable for future chapters (e.g., Chapter 2.0, 3.0) by focusing on general principles (e.g., control types, roles, threats) that can apply to new content.
- **Memory Utilization**: When prior Q/A sets are provided, use conversation memory to ensure new questions complement existing ones, maintaining a cohesive learning resource.