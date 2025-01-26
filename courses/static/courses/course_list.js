document.addEventListener('DOMContentLoaded', function () {
    // -----------------------------------------
    // "enroll-button" logic
    // -----------------------------------------
    const enrollButtons = this.querySelectorAll('.enroll-button');

    enrollButtons.forEach(button => {
        button.addEventListener('click', function() {
            const courseId = this.getAttribute('data-course-id');
            const form = this.nextElementSibling;
            form.style.display = 'block';
            this.style.display = 'none';
        });
    });

    // -----------------------------------------
    // Autocomplete logic
    // -----------------------------------------
    let suggestionItems = [];
    let currentIndex = -1;

    const searchInput = document.getElementById("searchInput");
    const suggestionsBox = document.getElementById("suggestionBox");
    const searchForm = document.getElementById("searchForm");

    // Fetch suggestions whenever user types
    searchInput.addEventListener("input", async function() {
        const query = this.value.trim();

        // If empty, hide suggestions
        if (!query) {
            suggestionsBox.innerHTML = "";
            suggestionsBox.style.display = "none";
            return;
        }

        try {
            const response = await fetch(`/courses/suggestions/?q=${encodeURIComponent(query)}`);
            const suggestions = await response.json();

            // Build suggestion UI
            if (suggestions.length > 0) {
                let htmlContent = "";
                suggestions.forEach(item => {
                    htmlContent += `<div class="suggestion-item" data-id="${item.id}">
                                        ${item.title}
                                    </div>`;
                    
                });
                suggestionBox.innerHTML = htmlContent;
                suggestionsBox.style.display = "block";
            } else {
                suggestionsBox.innerHTML = "<div class='no-suggestions'>No suggestions found</div>";
                suggestionsBox.style.display = "block";
            }

            // Grab all .suggestion-item elements
            suggestionItems = Array.from(suggestionsBox.querySelectorAll(".suggestion-item"));
            currentIndex = -1;
        } catch (err) {
            console.error("Error fetching suggestions:", err);
        }
    });

    // Click on a suggestion -> select it
    suggestionsBox.addEventListener("click", function(e) {
        if (e.target.classList.contains("suggestion-item")) {
            selectItem(e.target);
        }
    });

    // Keyboard navigation for the suggestions
    searchInput.addEventListener("keydown", function(e) {
        if (!suggestionItems || suggestionItems.length===0) return;

        switch (e.key) {
            case "ArrowDown":
                // e.preventDefault();
                currentIndex++;
                if (currentIndex >= suggestionItems.length) {
                    currentIndex = 0;
                }
                highlightItem(currentIndex);
                break;
            case "ArrowUp":
                // e.preventDefault();
                currentIndex--;
                if (currentIndex < 0) {
                    currentIndex = suggestionItems.length - 1;
                }
                highlightItem(currentIndex);
                break;
            case "Enter":
                // If an item is highlighten, select it
                if (currentIndex >= 0) {
                    // e.preventDefault();
                    selectItem(suggestionItems[currentIndex]);
                }
                break;
            default:
                break;
        }
    });


    // ----------------------------------------
    // Helper functions
    // ----------------------------------------
    function highlightItem(index) {
        // Remove highlight from all items
        suggestionItems.forEach(item => item.classList.remove("highlight"));
        // Highlight the current item
        suggestionItems[index].classList.add("highlight");
    }

    function selectItem(itemElement) {
        // Set input value to chosen suggestion
        const selectedTitle = itemElement.textContent.trim();
        searchInput.value = selectedTitle;

        // Hide suggestions
        suggestionBox.style.display = "none";

        // Auto-submit the search form
        searchForm.submit();
    }
});