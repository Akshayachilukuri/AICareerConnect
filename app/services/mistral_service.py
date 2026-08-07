import requests

class MistralService:
    """Service layer handling communication with the Mistral AI API."""
    
    def __init__(self, api_key=None, model="mistral-small-latest"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.mistral.ai/v1/chat/completions"

    def generate_chat_response(self, user_prompt, conversation_history=None, target_role="Software Engineer"):
        """Generates AI career advice response using Mistral API with fallback."""
        if not self.api_key:
            return self._fallback_chat_response(user_prompt, target_role)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_instruction = (
            f"You are an expert AI Career Coach specializing in helping candidates prepare for "
            f"target roles like {target_role}. Provide actionable, structured, encouraging, and clear guidance."
        )

        messages = [{"role": "system", "content": system_instruction}]

        if conversation_history:
            for msg in conversation_history:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": user_prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 800
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return self._fallback_chat_response(user_prompt, target_role)
        except Exception as e:
            return self._fallback_chat_response(user_prompt, target_role)

    def analyze_resume(self, resume_text, target_job):
        """Analyzes a resume against target job description."""
        prompt = (
            f"Analyze the following resume for a target role of '{target_job}'.\n"
            f"Resume Text:\n{resume_text}\n\n"
            f"Provide: 1) Match Score (0-100), 2) Key Skills Found, 3) Missing Skills, 4) Improvement Suggestions."
        )
        if not self.api_key:
            return self._fallback_resume_analysis(target_job)
        
        return self.generate_chat_response(prompt, target_role=target_job)

    def generate_interview_questions(self, role_title, count=3):
        """Generates realistic mock interview questions for a specific role."""
        if not self.api_key:
            return [
                f"Can you explain a challenging technical problem you solved while working as a {role_title}?",
                f"How do you approach system design and scalability in your current architecture?",
                f"Describe a situation where you had to negotiate requirements with non-technical stakeholders."
            ]
        
        prompt = f"Generate {count} technical and behavioral interview questions for a {role_title} position. Format as a clear numbered list."
        response = self.generate_chat_response(prompt, target_role=role_title)
        
        # Parse lines into list
        questions = [q.strip() for q in response.split('\n') if q.strip() and (q.strip()[0].isdigit() or q.strip().startswith('-'))]
        return questions if questions else [response]

    def _fallback_chat_response(self, user_prompt, target_role):
        """Fallback response generator if API key is not configured."""
        prompt_lower = user_prompt.lower()
        if "resume" in prompt_lower:
            return (
                f"To optimize your resume for a **{target_role}** role:\n"
                f"1. **Use Action Verbs**: Start bullets with 'Architected', 'Implemented', 'Optimized'.\n"
                f"2. **Quantify Metrics**: E.g., 'Reduced API latency by 40% using Redis caching'.\n"
                f"3. **Tailor Keywords**: Match technical skills mentioned in the job description."
            )
        elif "interview" in prompt_lower or "question" in prompt_lower:
            return (
                f"Here are key tips for **{target_role}** interviews:\n"
                f"• Use the **STAR Method** (Situation, Task, Action, Result) for behavioral questions.\n"
                f"• Speak your thought process out loud when solving technical challenges.\n"
                f"• Ask clarify questions before jumping into architecture or code."
            )
        elif "salary" in prompt_lower or "negotiat" in prompt_lower:
            return (
                f"For salary negotiation in a **{target_role}** position:\n"
                f"• Benchmark standard compensation using platforms like levels.fyi and Glassdoor.\n"
                f"• Focus on total compensation (Base + Equity + Signing Bonus)."
            )
        else:
            return (
                f"As your AI Career Coach for **{target_role}**, I recommend focusing on building projects, "
                f"practicing system design, and polishing your interview communication skills. "
                f"How can I assist your career progression today?"
            )

    def _fallback_resume_analysis(self, target_job):
        return (
            f"**Match Score**: 85/100\n\n"
            f"**Key Skills Found**: Python, Flask, SQL, REST APIs, Git\n\n"
            f"**Missing Skills**: Docker, CI/CD Pipelines, Kubernetes\n\n"
            f"**Suggestions**: Highlight measurable business impact for your target role as a {target_job}."
        )
