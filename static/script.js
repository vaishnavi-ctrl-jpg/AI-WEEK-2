document.addEventListener("DOMContentLoaded", () => {
    // Dom Elements
    const contextInput = document.getElementById("context-input");
    const highlightBackdrop = document.getElementById("highlight-backdrop");
    const questionInput = document.getElementById("question-input");
    const askBtn = document.getElementById("ask-btn");
    const loadDemoBtn = document.getElementById("load-demo-btn");
    const charCount = document.getElementById("char-count");
    const responseViewport = document.getElementById("response-viewport");
    const initialMessage = document.getElementById("initial-message");
    const modelStatusText = document.querySelector(".status-text");

    // State Tracker
    let isRequesting = false;

    // Sample Data
    const DEMO_TEXT = `Attention Is All You Need (Abstract)

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. 

Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.`;

    // 1. Realtime Context Handling
    function updateContextState() {
        const text = contextInput.value;
        charCount.textContent = text.length;
        
        // Sync text to hidden backdrop for highlighting structure
        syncBackdropText(text);

        // Enable/disable inquiry fields
        const isActive = text.trim().length > 20;
        questionInput.disabled = !isActive;
        askBtn.disabled = !isActive;

        if (isActive) {
            questionInput.placeholder = "Ask a question about this text...";
        } else {
            questionInput.placeholder = "Add more context to enable asking...";
        }
    }

    // 2. Scrolling and Content Sync for Custom Highlight Backdrop
    function syncBackdropText(text) {
        // Safely escape HTML inside the backdrop text to prevent raw injection
        const escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
        highlightBackdrop.innerHTML = escaped + "\n"; // match trailing whitespace
    }

    function syncScroll() {
        highlightBackdrop.scrollTop = contextInput.scrollTop;
        highlightBackdrop.scrollLeft = contextInput.scrollLeft;
    }

    contextInput.addEventListener("input", updateContextState);
    contextInput.addEventListener("scroll", syncScroll);

    // 3. Load Demo Btn
    loadDemoBtn.addEventListener("click", () => {
        contextInput.value = DEMO_TEXT;
        updateContextState();
        contextInput.focus();
    });

    // 4. Trigger Question Submission
    function submitQuestion() {
        const question = questionInput.value.trim();
        const context = contextInput.value.trim();

        if (!question || !context || isRequesting) return;

        // Hide initial helper placeholder if it exists
        if (initialMessage) {
            initialMessage.remove();
        }

        // Append User Bubble
        appendChatBubble("user", question);
        questionInput.value = ""; // Clear field
        
        // Add AI Thinking Bubble
        const thinkingBubble = appendThinkingBubble();
        setLoadingState(true);

        // API POST
        fetch("/api/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ context: context, question: question })
        })
        .then(async response => {
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.error || "Unknown server error");
            }
            return data;
        })
        .then(data => {
            // Remove thinking animation
            thinkingBubble.remove();

            // Extract coordinates and render AI Bubble
            appendChatBubble("ai", data.answer, {
                score: data.score,
                start: data.start,
                end: data.end
            });

            // Apply precise visual Highlight inside Context Textarea Backdrop
            applyTextHighlight(context, data.start, data.end);
        })
        .catch(err => {
            thinkingBubble.remove();
            appendChatBubble("ai", `⚠️ Error: ${err.message}`);
            console.error("Inquiry Error:", err);
        })
        .finally(() => {
            setLoadingState(false);
        });
    }

    // 5. Chat Bubble Rendering Utils
    function appendChatBubble(sender, text, meta = null) {
        const item = document.createElement("div");
        item.className = `chat-item ${sender}`;

        const label = document.createElement("div");
        label.className = "chat-label";
        label.textContent = sender === "user" ? "Inquiry" : "Oracle Response";

        const bubble = document.createElement("div");
        bubble.className = "chat-bubble";
        bubble.textContent = text;

        // If it contains metadata stats, append them
        if (meta) {
            const statBlock = document.createElement("div");
            statBlock.className = "answer-stat-block";
            
            const confidencePct = (meta.score * 100).toFixed(1) + "%";
            
            statBlock.innerHTML = `
                <div class="stat-item">Confidence: <span class="stat-val">${confidencePct}</span></div>
                <div class="stat-item">Span Index: <span class="stat-val">${meta.start}-${meta.end}</span></div>
            `;
            bubble.appendChild(statBlock);
        }

        item.appendChild(label);
        item.appendChild(bubble);
        
        responseViewport.appendChild(item);
        responseViewport.scrollTop = responseViewport.scrollHeight;

        return item;
    }

    function appendThinkingBubble() {
        const item = document.createElement("div");
        item.className = "chat-item ai";

        const label = document.createElement("div");
        label.className = "chat-label";
        label.textContent = "Computing Oracle Network";

        const bubble = document.createElement("div");
        bubble.className = "chat-bubble";
        bubble.innerHTML = `
            <div class="thinking-dots">
                <span></span><span></span><span></span>
            </div>
        `;

        item.appendChild(label);
        item.appendChild(bubble);
        responseViewport.appendChild(item);
        responseViewport.scrollTop = responseViewport.scrollHeight;

        return item;
    }

    // 6. In-Text Backdrop Highlighter
    function applyTextHighlight(context, start, end) {
        if (start === undefined || end === undefined) return;
        
        // Re-escape the whole text, then carefully slice in the <mark> tags
        // Splitting string into: before mark, exact token, and after mark.
        const before = context.substring(0, start);
        const token = context.substring(start, end);
        const after = context.substring(end);

        const escape = (str) => str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

        highlightBackdrop.innerHTML = 
            escape(before) + 
            `<mark class="ai-highlight">${escape(token)}</mark>` + 
            escape(after) + "\n";
            
        // Scroll the highlight into view inside the backdrop if needed
        const markEl = highlightBackdrop.querySelector(".ai-highlight");
        if (markEl) {
            // Calculate offset and trigger visual scrolls
            setTimeout(() => {
                const relativeOffset = markEl.offsetTop - 40;
                contextInput.scrollTo({ top: relativeOffset, behavior: 'smooth' });
            }, 200);
        }
    }

    // 7. UI State management
    function setLoadingState(loading) {
        isRequesting = loading;
        askBtn.disabled = loading;
        questionInput.disabled = loading;

        const btnText = askBtn.querySelector(".btn-text");
        const btnLoader = askBtn.querySelector(".btn-loader");

        if (loading) {
            btnText.style.visibility = "hidden";
            btnLoader.style.display = "block";
            modelStatusText.textContent = "Neural Network Active...";
        } else {
            btnText.style.visibility = "visible";
            btnLoader.style.display = "none";
            modelStatusText.textContent = "Transformers Engine Active";
            questionInput.focus();
        }
    }

    // Bind Actions
    askBtn.addEventListener("click", submitQuestion);
    questionInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
            submitQuestion();
        }
    });
});
