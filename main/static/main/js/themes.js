// Функция установки темы
function setTheme(themeName, isInitialLoad = false) {
    console.log('Setting theme to:', themeName, 'Initial load:', isInitialLoad);
    
    const prevTheme = document.body.className;
    document.body.className = themeName;
    localStorage.setItem('theme', themeName);
    
    // Активируем соответствующую кнопку в меню и переключателе
    updateThemeUI(themeName);
    
    // Обновляем мета-тег темы для браузера
    updateMetaThemeColor(getThemeColor(themeName));
    
    // Проверяем, была ли тема уже установлена в этой сессии (для подавления повторных уведомлений)
    const sessionInitialized = sessionStorage.getItem('themeInitialized');
    
    // Показываем уведомление только если:
    // 1. Это НЕ начальная загрузка страницы
    // 2. Тема действительно изменилась
    // 3. Сессия уже была инициализирована
    if (!isInitialLoad && prevTheme !== themeName && sessionInitialized) {
        showThemeNotification(getThemeNameRu(themeName));
        console.log('Theme changed from', prevTheme, 'to', themeName);
    }
    
    // Отмечаем, что тема была инициализирована
    sessionStorage.setItem('themeInitialized', 'true');
    
    // Создаем событие изменения темы для других скриптов
    const event = new CustomEvent('themeChanged', { detail: { theme: themeName } });
    document.dispatchEvent(event);
}

// Вспомогательная функция для получения названия темы на русском
function getThemeNameRu(themeName) {
    if (themeName === 'dark-theme') return 'Темная';
    if (themeName === 'minecraft-theme') return 'Minecraft';
    return 'Светлая';
}

// Вспомогательная функция для получения цвета темы
function getThemeColor(themeName) {
    if (themeName === 'dark-theme') return '#121212';
    if (themeName === 'minecraft-theme') return '#5c8d44';
    return '#ffffff';
}

// Вспомогательная функция для обновления UI
function updateThemeUI(themeName) {
    // Обновляем плавающие кнопки
    const buttons = document.querySelectorAll('.theme-btn');
    buttons.forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-theme') === themeName || (themeName === '' && btn.classList.contains('light-theme-btn')));
    });
    
    // Обновляем пункты меню в шапке
    const menuItems = document.querySelectorAll('.dropdown-item[class*="theme-switcher-"]');
    menuItems.forEach(item => {
        const itemTheme = item.getAttribute('data-theme') || '';
        item.classList.toggle('active', itemTheme === themeName);
    });
}

// Функция обновления мета-тега цвета темы для мобильных браузеров
function updateMetaThemeColor(color) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
        metaThemeColor = document.createElement('meta');
        metaThemeColor.name = 'theme-color';
        document.head.appendChild(metaThemeColor);
    }
    metaThemeColor.content = color;
}

// Функция добавления класса для анимации перехода
function addTransitionClass() {
    document.body.classList.add('theme-transition');
    setTimeout(() => {
        document.body.classList.remove('theme-transition');
    }, 1000);
}

// Функция для отображения уведомления о смене темы
function showThemeNotification(themeName) {
    const existingNotification = document.querySelector('.theme-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = 'theme-notification';
    notification.textContent = `Тема изменена на "${themeName}"`;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');
    
    // Инициализация темы (isInitialLoad = true)
    if (savedTheme !== null) {
        setTheme(savedTheme, true);
    } else if (prefersDarkMode) {
        setTheme('dark-theme', true);
    } else {
        setTheme('', true);
    }
    
    // Обработчики для меню
    const themeMenuItems = document.querySelectorAll('.dropdown-item[class*="theme-switcher-"]');
    themeMenuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const theme = e.currentTarget.getAttribute('data-theme') || '';
            addTransitionClass();
            setTheme(theme);
        });
    });
    
    // Добавляем переключатель тем, если его еще нет
    if (!document.querySelector('.theme-switcher')) {
        const themeSwitcher = document.createElement('div');
        themeSwitcher.className = 'theme-switcher';
        
        const themes = [
            { id: 'light', icon: 'bi-brightness-high-fill', theme: '', label: 'Светлая', title: 'Alt+1' },
            { id: 'dark', icon: 'bi-moon-fill', theme: 'dark-theme', label: 'Темная', title: 'Alt+2' },
            { id: 'minecraft', icon: 'bi-grid-3x3-gap-fill', theme: 'minecraft-theme', label: 'Minecraft', title: 'Alt+3' }
        ];
        
        themes.forEach(t => {
            const btn = document.createElement('button');
            btn.className = `theme-btn ${t.id}-theme-btn`;
            btn.title = `${t.label} тема (${t.title})`;
            btn.setAttribute('aria-label', `Включить ${t.label} тему`);
            btn.setAttribute('data-theme', t.theme);
            btn.innerHTML = `<i class="bi ${t.icon}"></i>`;
            btn.addEventListener('click', () => {
                addTransitionClass();
                setTheme(t.theme);
            });
            themeSwitcher.appendChild(btn);
        });
        
        document.body.appendChild(themeSwitcher);
        
        document.addEventListener('keydown', function(event) {
            if (event.altKey) {
                if (event.key === '1') { addTransitionClass(); setTheme(''); event.preventDefault(); }
                else if (event.key === '2') { addTransitionClass(); setTheme('dark-theme'); event.preventDefault(); }
                else if (event.key === '3') { addTransitionClass(); setTheme('minecraft-theme'); event.preventDefault(); }
            }
        });
    }
    
    // Синхронизация между вкладками
    window.addEventListener('storage', (event) => {
        if (event.key === 'theme') {
            setTheme(event.newValue || '', true); // true, чтобы не показывать уведомление
        }
    });

    // Изменение системной темы
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
            if (!localStorage.getItem('theme')) {
                setTheme(event.matches ? 'dark-theme' : '', true);
            }
        });
    }
    
    console.log('Theme system initialized. Current theme:', document.body.className || 'default (light)');
});