function showImageModal(src) {
    var modal = document.getElementById("imageModal");
    var modalImg = document.getElementById("modalImage");
    modal.style.display = "block";
    modalImg.src = src;
}
function closeModal() {
    document.getElementById("imageModal").style.display = "none";
}
