window.onload = function() {
  // チャットボックスを取得
  const chatBox = document.getElementById('chat-box');
  
  // チャットボックスのスクロールを一番下に設定
  if (chatBox) {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Ctrl + Enterでフォームを送信
  const form = document.getElementById('chat-form');
  const textarea = document.getElementById('user-input');

  if (form && textarea) {
    textarea.addEventListener('keydown', function(event) {
        // Ctrl + Enterが押された場合
        if (event.ctrlKey && event.key === 'Enter') {
            event.preventDefault();  // デフォルトの動作（改行など）を防止
            form.submit();  // フォームを送信
        }
    });
  }

  // 折り畳み機能
  const toggleButton = document.getElementById('toggle-button');
  const characterContainer = document.querySelector('.character-container');

  if (toggleButton && characterContainer) {
    // 初期状態の設定（localStorage から復元、デフォルトは折り畳み状態）
    const isCollapsed = localStorage.getItem('characterPanelCollapsed') !== 'false';
    
    if (isCollapsed) {
      // 折り畳み状態（初期値）
      characterContainer.classList.add('collapsed');
      toggleButton.innerHTML = '▶';
    } else {
      // 展開状態
      characterContainer.classList.remove('collapsed');
      toggleButton.innerHTML = '◀';
    }

    toggleButton.addEventListener('click', function() {
      const isCurrentlyCollapsed = characterContainer.classList.contains('collapsed');
      
      if (isCurrentlyCollapsed) {
        // 折り畳み状態から展開する
        characterContainer.classList.remove('collapsed');
        toggleButton.innerHTML = '◀';
        localStorage.setItem('characterPanelCollapsed', 'false');
      } else {
        // 展開状態から折り畳む
        characterContainer.classList.add('collapsed');
        toggleButton.innerHTML = '▶';
        localStorage.setItem('characterPanelCollapsed', 'true');
      }
    });
  }
}