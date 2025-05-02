class FileUploader {
    constructor(dropzone) {
        this.dropzone = dropzone;
        this.input = dropzone.querySelector('.file-input');
        this.preview = dropzone.querySelector('.file-preview');
        this.files = [];

        // Configuration options from data attributes
        this.allowedTypes = (this.input.accept || '').split(',').map(s => s.trim().toLowerCase());
        this.maxFileSize = parseInt(this.input.dataset.maxSize || '0', 10); // Max file size in bytes
        this.maxTotalSize = parseInt(this.input.dataset.maxTotalSize || '0', 10); // Max total size in bytes
        this.maxFiles = parseInt(this.input.dataset.maxFiles || '0', 10); // Max number of files

        // Initialize the uploader
        this.init();
        this.initializeExistingFiles();
    }

    // Initializes event listeners for the dropzone and input file interactions
    init() {
        this.dropzone.addEventListener('click', () => this.input.click());

        this.input.addEventListener('change', e => this.addFiles(e.target.files));

        this.dropzone.addEventListener('dragover', e => {
            e.preventDefault();
            this.dropzone.classList.add('dragover');
        });

        this.dropzone.addEventListener('dragleave', () => {
            this.dropzone.classList.remove('dragover');
        });

        this.dropzone.addEventListener('drop', e => {
            e.preventDefault();
            this.dropzone.classList.remove('dragover');
            this.addFiles(e.dataTransfer.files);
        });
    }

    // Initialize files that may have been pre-selected in the file input (e.g., on page reload)
    initializeExistingFiles() {
        if (this.input.files.length > 0) {
            Array.from(this.input.files).forEach(file => {
                if (this.isFileTypeAllowed(file)) {
                    this.files.push(file);
                    this.renderPreviews();
                    this.updateFileInfo();
                }
            });
        }
    }

    // Validate the file type against the allowed types and extensions
    isFileTypeAllowed(file) {
        const type = file.type.toLowerCase();
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        return this.allowedTypes.length === 0 || this.allowedTypes.some(allowed =>
            allowed === type || allowed === ext || (allowed.endsWith('/*') && type.startsWith(allowed.split('/')[0]))
        );
    }

    // Get the total size of the files in the input
    getTotalSize() {
        return this.files.reduce((sum, file) => sum + file.size, 0);
    }

    // Add new files to the file list, while checking for size, type, and duplication
    addFiles(newFiles) {
        const filesArray = Array.from(newFiles);
        const rejected = [];

        filesArray.forEach(file => {
            const isDuplicate = this.files.some(f => f.name === file.name && f.size === file.size);
            const isTypeOk = this.isFileTypeAllowed(file);
            const isSizeOk = this.maxFileSize === 0 || file.size <= this.maxFileSize;
            const withinLimit = this.maxFiles === 0 || this.files.length < this.maxFiles;
            const totalSizeOk = this.maxTotalSize === 0 || (this.getTotalSize() + file.size <= this.maxTotalSize);

            if (!isDuplicate && isTypeOk && isSizeOk && withinLimit && totalSizeOk) {
                this.files.push(file);
            } else {
                rejected.push(file);
            }
        });

        this.updateInputFiles();
        this.renderPreviews();
        this.updateFileInfo();

        if (rejected.length) {
            alert(`${rejected.length} file(s) were rejected due to type, size, count, or duplicates.`);
        }
    }

    // Update the file input element with the current files array
    updateInputFiles() {
        const dt = new DataTransfer();
        this.files.forEach(file => dt.items.add(file));
        this.input.files = dt.files;
    }

    // Render file previews in the preview container
    renderPreviews() {
        this.preview.innerHTML = ''; // Clear existing previews
        this.files.forEach((file, i) => {
            const item = document.createElement('div');
            item.className = 'file-item';

            // Image preview
            if (file.type.startsWith('image/')) {
                const img = document.createElement('img');
                img.src = URL.createObjectURL(file);
                img.onload = () => URL.revokeObjectURL(img.src);
                item.appendChild(img);
            } else {
                // Generic file icon for non-image files
                const icon = document.createElement('div');
                icon.className = 'file-icon';
                icon.innerHTML = '📄'; // Placeholder icon (replace with hero icons if needed)
                item.appendChild(icon);
            }

            // File name and size
            const name = document.createElement('div');
            name.className = 'file-name';
            name.textContent = file.name;
            item.appendChild(name);

            const size = document.createElement('div');
            size.className = 'file-size';
            size.textContent = `${(file.size / 1024).toFixed(1)} KB`;
            item.appendChild(size);

            // Remove button
            const removeBtn = document.createElement('button');
            removeBtn.className = 'remove-btn';
            removeBtn.innerHTML = '&times;';
            removeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                this.removeFile(i);
            });
            item.appendChild(removeBtn);

            // Replace file if clicked (not on remove button)
            item.addEventListener('click', e => {
                if (e.target !== removeBtn) this.replaceFile(i);
            });

            this.preview.appendChild(item);
        });
    }

    // Remove a file from the list and update the UI
    removeFile(index) {
        this.files.splice(index, 1);
        this.updateInputFiles();
        this.renderPreviews();
        this.updateFileInfo();
    }

    // Replace an existing file with a new file selected through a temporary input
    replaceFile(index) {
        const tempInput = document.createElement('input');
        tempInput.type = 'file';
        tempInput.accept = this.input.accept;
        tempInput.addEventListener('change', () => {
            const file = tempInput.files[0];
            if (!file) return;

            // Validate the new file
            const isDuplicate = this.files.some((f, i) => i !== index && f.name === file.name && f.size === file.size);
            const isTypeOk = this.isFileTypeAllowed(file);
            const isSizeOk = this.maxFileSize === 0 || file.size <= this.maxFileSize;
            const totalSizeOk = this.maxTotalSize === 0 || (this.getTotalSize() - this.files[index].size + file.size <= this.maxTotalSize);

            if (!isDuplicate && isTypeOk && isSizeOk && totalSizeOk) {
                this.files[index] = file;
                this.updateInputFiles();
                this.renderPreviews();
                this.updateFileInfo();
            } else {
                alert("File rejected due to type, size, or duplication.");
            }
        });

        tempInput.click(); // Trigger file selection dialog
    }

    // Update the file info display with the current upload statistics
    updateFileInfo() {
        const fileCount = this.files.length;
        const totalSize = this.getTotalSize();
        const maxFiles = this.maxFiles;
        const maxTotalSize = this.maxTotalSize / 1024 / 1024; // MB
        const maxFileSize = this.maxFileSize / 1024; // KB

        this.dropzone.querySelector('.file-info-message').textContent = `Total files uploaded: ${fileCount} / Max files: ${maxFiles}`;
        this.dropzone.querySelector('.file-size-info').textContent = `Total size uploaded: ${(totalSize / 1024).toFixed(1)} KB / Max total size: ${maxTotalSize.toFixed(1)} MB`;
    }
}

// Initialize
document.querySelectorAll('.file-dropzone').forEach(dropzone => {
    new FileUploader(dropzone);
});