const boardDiv = document.getElementById("board");


function renderBoard(board) {
    boardDiv.innerHTML = "";
    board.forEach((row, r) => {
        row.forEach((val, c) => {
            const input = document.createElement("input");
            input.className = "cell";
            input.maxLength = 1;
            input.value = val === 0 ? "" : val;
            if (val !== 0) input.disabled = true;

            input.oninput = () => {
                const val = input.value;

    // Remove anything that is not 1–9
                if (!/^[1-9]?$/.test(val)) {
                    input.value = "";
                    input.classList.add("invalid");
                    return;
                }

    input.classList.remove("invalid");
    START_BOARD[r][c] = val === "" ? 0 : parseInt(val);

    validateCell(r, c);
};


            boardDiv.appendChild(input);
        });
    });
}
let startTime = Date.now();

setInterval(() => {
    const seconds = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById("timer").innerText = `Time: ${seconds}s`;
}, 1000);

function checkBoard() {
    fetch("/check", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({board: START_BOARD})
    })
    .then(res => res.json())
    .then(data => {
        if (!data.valid) {
            alert("Invalid move");
        } else if (data.solved) {
            alert(`Solved!\nTime: ${data.time}s\nScore: ${data.score}`);
        } else {
            alert("Correct so far!");
        }
    });
}


function getHint() {
    fetch("/hint", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({board: START_BOARD})
    })
    .then(res => {
        if (!res.ok) throw res;
        return res.json();
    })
    .then(data => {
        const [r, c, num] = data.hint;
        START_BOARD[r][c] = num;
        document.getElementById("hints").innerText =
            `Hints left: ${data.remaining}`;
        renderBoard(START_BOARD);
    })
    .catch(() => {
        alert("No hints remaining");
    });
}

function newGame() {
    location.reload();
}

renderBoard(START_BOARD);
