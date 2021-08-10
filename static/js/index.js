// File Upload

function ekUpload() {
    const fileSelect = document.getElementById("file-upload"),
        fileDrag = document.getElementById("file-drag"),
        m = document.getElementById("messages"),
        filePreview = document.getElementById("file-txt"),
        results = document.getElementById("results"),
        closeBtn = document.getElementById("close"),
        fileForm = document.getElementById("file-upload-form"),
        toHideFailure = [document.getElementById("parsed"), closeBtn],
        toHideSuccess = [
            document.getElementById("start"),
            document.getElementById("start"),
            document.getElementById("nottxt")
        ];

    let id = 0;

    const crc_poly = "1011",
        lrc_bits = 8,
        cks_bits = 16,
        vrc_parity = "Even";

    function Init() {
        fileSelect.addEventListener("change", fileSelectHandler, false);
        fileDrag.addEventListener("dragover", fileDragHover, false);
        fileDrag.addEventListener("dragleave", fileDragHover, false);
        fileDrag.addEventListener("drop", fileSelectHandler, false);
        closeBtn.addEventListener("click", () => {
            filePreview.classList.add("hidden");
            toHideFailure.forEach((el) => el.classList.add("hidden"));
            toHideSuccess.forEach((el) => el.classList.remove("hidden"));
            document.getElementById("nottxt").classList.add("hidden");
            fileForm.reset();
        });
    }

    function fileDragHover(e) {
        e.stopPropagation();
        e.preventDefault();
        fileDrag.className =
            e.type === "dragover" ? "hover" : "modal-body file-upload";
    }

    async function fileSelectHandler(e) {
        const files = e.target.files || e.dataTransfer.files;
        fileDragHover(e);
        for (let i = 0, f; (f = files[i]); i++) {
            await parseUploadFile(f);
        }
    }

    function output(msg) {
        m.innerHTML = msg;
    }

    function verifyFileText(text) {
        return text && !/[^1,0]+/g.test(text);
    }

    async function parseUploadFile(file) {
        const txtName = file.name;
        console.log("Name: ", txtName);
        output("<strong>" + txtName + "</strong>");

        const fileText =
            /\.(?=txt|text|bin)/gi.test(txtName) && (await file.text());
        if (verifyFileText(fileText)) {
            const d = document.createElement("div");
            d.id = `table-${id}`;
            id += 1;
            d.innerHTML = `<p><img src="/static/img/Spinner.svg" alt="Loading" height="200px" width="200px" focus></p>`;
            results.appendChild(d);
            toHideSuccess.forEach((el) => el.classList.add("hidden"));
            toHideFailure.forEach((el) => el.classList.remove("hidden"));
            // Preview
            console.log("Text: ", fileText);
            filePreview.classList.remove("hidden");
            filePreview.innerHTML = fileText;
            await uploadFile(txtName, fileText, d);
        } else {
            filePreview.classList.add("hidden");
            toHideFailure.forEach((el) => el.classList.add("hidden"));
            toHideSuccess.forEach((el) => el.classList.remove("hidden"));
            fileForm.reset();
        }
    }

    function successFailureNotify(err, res, nc) {
        return `
            <td class="bg-${(err === "None" || nc )|| !res ? "success" : "failure"}">
            </td>
            `;
    }

    function createResultTable(initial, filename, results, time) {
        return `
            <table>
                <thead>
                    <th colspan="3">
                        Filename: "${filename}"
                        processed in ${time} milliseconds
                    </th>
                </thead>
                <thead>
                    <th colspan="3" class="bg-errtype">Error type: ${
                        results.error_type
                    }</th>
                </thead>
                <thead>
                    <th>
                        Error Control
                    </th>
                    <th>
                        Time to check
                    </th>
                    <th>
                        Successfully detected
                    </th>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            VRC
                        </td>
                        <td>
                            ${results.vrc.time / 1000} ms
                        </td>
                        ${successFailureNotify(
                            results.error_type,
                            results.vrc.success,
                            results.vrc.data === initial.vrc.data
                        )}
                    </tr>
                    <tr>
                        <td>
                            LRC
                        </td>
                        <td>
                            ${results.lrc.time / 1000} ms
                        </td>
                        ${successFailureNotify(
                            results.error_type,
                            results.lrc.success,
                            results.lrc.data === initial.lrc.data
                        )}
                    </tr>
                    <tr>
                        <td>
                            CRC
                        </td>
                        <td>
                            ${results.crc.time / 1000} ms
                        </td>
                        ${successFailureNotify(
                            results.error_type,
                            results.crc.success,
                            results.crc.data === initial.crc.data
                        )}
                    </tr>
                    <tr>
                        <td>
                            Checksum
                        </td>
                        <td>
                            ${results.cks.time / 1000} ms
                        </td>
                        ${successFailureNotify(
                            results.error_type,
                            results.cks.success,
                            results.cks.data === initial.cks.data
                        )}
                    </tr>
                </tbody>
            </table>
        `;
    }

    async function uploadFile(fn, text, resultDiv) {
        console.log("upload called");
        results.scrollIntoView({ behavior: "smooth" });
        const vr = vrc(text, vrc_parity),
            lr = lrc(text, lrc_bits),
            cr = crc(text, crc_poly),
            cs = cks(text, cks_bits);
        console.log("vrc", vr);
        console.log("lrc", lr);
        console.log("crc", cr);
        console.log("cks", cs);
        const d0 = Date.now();
        const initdata = {
            vrc: { data: vr, meta: { parity: vrc_parity } },
            lrc: { data: lr, meta: { bits: lrc_bits } },
            crc: { data: cr, meta: { poly: crc_poly } },
            cks: { data: cs, meta: { bits: cks_bits } },
            data: text
        };
        try {
            const r = await fetch(fileForm.getAttribute("action"), {
                method: "POST",
                // const r = await fetch("/res.json", {
                //     method: "GET",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(initdata)
            });
            const rj = await r.json();
            console.log(rj, `${Date.now() - d0} miliseconds`);
            resultDiv.innerHTML = createResultTable(initdata, fn, rj, Date.now() - d0);
        } catch (error) {
            resultDiv.innerHTML = `<p class="bg-failure">Sorry, an error occured!!</p>`;
            console.log(error);
        }
    }

    // Check for the constious File API support.
    if (window.File && window.FileList && window.FileReader && window.fetch) {
        Init();
    } else {
        document.getElementById("file-drag").style.display = "none";
    }
}
ekUpload();
