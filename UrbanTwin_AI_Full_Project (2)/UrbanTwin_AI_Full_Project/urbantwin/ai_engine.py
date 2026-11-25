"""Gemini LLM integration with deterministic fallback."""
import os
from dotenv import load_dotenv
from .recommendations import recommend
load_dotenv()

def fallback_analysis(category, params, result):
    recs=recommend(category,result,params)
    lines="\n".join(f"- **{r['title']}**: {r['reason']}" for r in recs)
    return (f"### Scenario explanation\n{result['explanation']}\n\n"
            f"### Possible causes and impacts\nThe selected inputs indicate a potential service pressure classified as **{result['severity']}** by the prototype's illustrative thresholds. "
            f"The baseline indicator is {result['baseline']} {result['unit']} and the projected indicator is {result['projected']} {result['unit']}. "
            f"These values are calculated by the application; they are not independent AI estimates.\n\n"
            f"### Recommended actions\n{lines}\n\n"
            f"### Short-term actions\nMonitor high-pressure locations, verify the input data and prioritise operational improvements that can be tested quickly.\n\n"
            f"### Long-term actions\nInvest in reliable data collection, infrastructure planning, demand management and periodic model calibration.\n\n"
            f"### Trade-offs and sustainability\nEvaluate cost, equity, environmental effects, service reliability and unintended consequences. Validate every action with local experts and stakeholders.")

def analyse_with_ai(category, params, result):
    key=os.getenv("GEMINI_API_KEY","").strip()
    if not key:
        return fallback_analysis(category,params,result) + "\n\n*Local fallback mode: configure GEMINI_API_KEY to enable LLM-generated analysis.*"
    try:
        from google import genai
        client=genai.Client(api_key=key)
        prompt=f"""You are UrbanTwin AI, a cautious smart-city decision-support assistant.
Use ONLY the provided simulation values for numerical claims. Never invent or alter numerical statistics.
Explain the problem and possible causes, impacts, short-term and long-term actions, trade-offs, sustainability and data needed for validation.
State that the model is simplified and inputs are hypothetical. Do not claim that interventions are guaranteed.
Scenario: {category}
Input parameters (user-entered): {params}
Application-calculated result: {result}
Return concise, well-structured Markdown."""
        model=os.getenv("GEMINI_MODEL","gemini-2.5-flash")
        response=client.models.generate_content(model=model,contents=prompt)
        return response.text or fallback_analysis(category,params,result)
    except Exception:
        return fallback_analysis(category,params,result) + "\n\n*LLM service was unavailable; local fallback recommendations are shown.*"
