# LLM Performance Analysis Report Generation Prompt

## Task
Generate a comprehensive technical report analyzing Large Language Model (LLM) performance on parallel code generation tasks, similar to the "Qwen 2.5: Efficient High Performance Code Generation at 1/50th of the VRAM" report. Focus on H2loop v0.1 model.

Here are absolute stats for resource requirements for running the models
| Model | Size | VRAM Requirements (Approx.)
|-------|------|------------------|
| **H2LooP v0.1** | 32B (4-bit quantized) | **16 GB** |
| **Qwen 2.5 Coder 32B** | 32B | **32 GB** | 
| **Gemini 2.5 Pro** | Unknown | **N/A** |
| **Gemini 2.5 Flash** | Unknown | **N/A** |
| **Llama-4 Maverick 400B** | 400B | **1,280 GB** |
| **Kimi-K2 Instruct 1T** | 1T | **1,024 GB** |
| **Llama 3.3 8B** | 8B | **16 GB** |
| **Mistral NeMo 12B** | 12B | **24 GB** |
| **Gemma-3 27B** | 27B | **54 GB** |
| **Gemma-3 27B** | 27B (4-bit quantized) | **19 GB** |


## Input Data Format
You will receive a CSV file (`raw_metrics.csv`) with the following columns:
- `model`: LLM model name
- `problem_type`: Computational domain (e.g., geometry, dense_la, fft, graph, etc.)
- `problem_name`: Specific problem identifier
- `parallelism_model`: Either "serial" or "mpi"
- `response_time`: Time taken to generate response (seconds)
- `total_tokens`: Total tokens in response
- `prompt_tokens`: Tokens in input prompt
- `source_write_success`: Boolean - code was successfully written
- `did_build`: Boolean - code compiled successfully
- `is_source_valid`: Boolean - source code is syntactically valid
- `did_any_run`: Boolean - at least one execution succeeded
- `did_all_run`: Boolean - all executions succeeded
- `are_any_valid`: Boolean - at least one execution produced valid results
- `are_all_valid`: Boolean - all executions produced valid results
- `best_runtime`: Fastest execution time (seconds)
- `avg_runtime`: Average execution time (seconds)
- `speedup_2proc`: Speedup factor with 2 MPI processes
- `speedup_4proc`: Speedup factor with 4 MPI processes
- `num_successful_runs`: Number of successful execution runs

## Report Structure Requirements

### 1. Performance Analysis Results

#### 1.1 Overall Performance Metrics
- **Build Success Rate Table**: Show `did_build` percentages by model for serial/MPI/combined
- **Validation Success Rate Table**: Show `are_all_valid` percentages by model (among successfully built code)
- **Performance Tier Analysis**: Categorize models into performance tiers with rationale

#### 1.2 Resource Efficiency Analysis
- **Performance per Resource Metric**: If VRAM data available, calculate efficiency ratios
- **Key Efficiency Findings**: Highlight most resource-efficient models

#### 1.3 Domain-Specific Performance
- **Domain Strengths Table**: Show success rates by problem domain for top-performing models
- **Performance Pattern Analysis**: Identify where models excel vs struggle
- **Strategic Insights**: Explain performance patterns and their implications

### 2. Advanced Statistical Analysis

#### 2.1 Confidence Intervals
- **Methodology Explanation**: Explain what confidence intervals are and why they matter for LLM evaluation
- **95% CI Table**: Calculate and present confidence intervals for key metrics
- **Interpretation**: Explain what the intervals reveal about model reliability

#### 2.2 Effect Size Analysis (Cohen's d) - compare this with H2LooP model 
- **Methodology Explanation**: Explain effect size, its importance, and interpretation scale
- **Comparison Matrix**: Calculate Cohen's d comparing all models against a reference model
- **Practical Significance**: Interpret which differences are meaningful vs statistical noise

### 3. Technical Deep Dive

#### 3.1 Runtime Performance Analysis
- **Serial Code Performance**: Statistics for successful serial executions
- **MPI Code Performance**: Statistics for successful parallel executions
- **Scaling Behavior**: Analysis of MPI speedup factors

#### 3.2 Response Time and Token Efficiency
- **Response Time Statistics**: Mean, median, std dev by model
- **Token Usage Analysis**: Efficiency metrics (success rate per token)
- **Speed vs Quality Trade-offs**: Correlation analysis

### 4. Research Implications

#### 4.1 Theoretical Contributions
- **Model Architecture Insights**: What the results reveal about different model designs
- **Quantization/Optimization Effects**: Impact of model optimizations on performance

#### 4.2 Practical Applications
- **Deployment Scenarios**: Optimal use cases for each model tier
- **Performance Optimization Strategies**: Recommended approaches

#### 4.3 Limitations and Future Work
- **Current Constraints**: Acknowledge limitations in the evaluation
- **Future Research Directions**: Suggest next steps for investigation

### 5. Conclusions
- **Key Findings Summary**: Restate primary contributions
- **Strategic Recommendations**: Actionable advice for researchers and practitioners
- **Final Assessment**: Overall evaluation with nuanced perspective

## Statistical Analysis Requirements

### Essential Calculations
1. **Success Rate Percentages**: Calculate for each metric by model and parallelism type
2. **Confidence Intervals**: Use 95% CI with appropriate t-distribution
3. **Effect Sizes**: Calculate Cohen's d for pairwise model comparisons
4. **Domain Analysis**: Success rates broken down by problem type
5. **Efficiency Metrics**: Performance per resource unit (if resource data available)

### Statistical Rigor
- **Sample Size Validation**: Ensure adequate sample sizes for statistical tests
- **Missing Data Handling**: Explicitly handle null/missing values
- **Assumption Checking**: Validate statistical assumptions (normality, independence)
- **Multiple Comparisons**: Consider correction for multiple statistical tests

## Writing Style Guidelines

### Technical Precision
- Use precise statistical terminology
- Include confidence levels and significance tests
- Provide exact numbers with appropriate precision
- Reference methodology for all calculations

### Clarity and Accessibility
- Explain statistical concepts for non-expert readers
- Use clear section headers and bullet points
- Include interpretation alongside raw statistics
- Balance technical depth with readability

### Professional Presentation
- Use tables and structured data presentation
- Include methodology explanations for complex analyses
- Provide actionable insights and recommendations
- Maintain objective, evidence-based tone

## Output Format
Generate a complete markdown report following the structure above, with:
- Proper markdown formatting (headers, tables, lists)
- Statistical tables with aligned columns
- Clear section numbering
- Professional academic writing style
- Comprehensive analysis covering all major aspects of the data

## Key Success Criteria
1. **Comprehensive Coverage**: Address all major performance dimensions
2. **Statistical Rigor**: Include proper statistical analysis with confidence intervals and effect sizes
3. **Practical Insights**: Provide actionable recommendations based on findings
4. **Clear Communication**: Make complex statistical concepts accessible
5. **Professional Quality**: Match the depth and sophistication of the reference report

The final report should be publication-ready and suitable for technical audiences including researchers, practitioners, and decision-makers in AI/ML deployment.