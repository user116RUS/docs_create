// Функция установки темы
function setTheme(themeName) {
    console.log('Setting theme to:', themeName);
    
    const prevTheme = document.body.className;
    document.body.className = themeName;
    localStorage.setItem('theme', themeName);
    
    // Активируем соответствующую кнопку
    const buttons = document.querySelectorAll('.theme-btn');
    buttons.forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Обновляем состояние пунктов меню
    // Сначала удаляем класс active у всех пунктов меню
    const menuItems = document.querySelectorAll('.dropdown-item[class*="theme-switcher-"]');
    menuItems.forEach(item => {
        item.classList.remove('active');
    });
    
    let themeName_ru = '';
    let themeColor = '';
    let activeSelector = '';
    
    if (themeName === '') {
        // Светлая тема
        document.querySelector('.light-theme-btn')?.classList.add('active');
        activeSelector = '.theme-switcher-light';
        themeColor = '#ffffff';
        themeName_ru = 'Светлая';
    } else if (themeName === 'dark-theme') {
        // Темная тема
        document.querySelector('.dark-theme-btn')?.classList.add('active');
        activeSelector = '.theme-switcher-dark';
        themeColor = '#121212';
        themeName_ru = 'Темная';
    } else if (themeName === 'minecraft-theme') {
        // Minecraft тема
        document.querySelector('.minecraft-theme-btn')?.classList.add('active');
        activeSelector = '.theme-switcher-minecraft';
        themeColor = '#5c8d44';
        themeName_ru = 'Minecraft';
    }
    
    // Активируем соответствующий пункт в меню
    console.log('Activating menu item:', activeSelector);
    const activeMenuItem = document.querySelector(activeSelector);
    if (activeMenuItem) {
        activeMenuItem.classList.add('active');
        console.log('Menu item activated');
    } else {
        console.log('Menu item not found');
    }
    
    // Обновляем мета-тег темы для браузера
    updateMetaThemeColor(themeColor);
    
    // Если тема изменилась, показываем уведомление
    if (prevTheme !== themeName) {
        showThemeNotification(themeName_ru);
        console.log('Theme changed from', prevTheme, 'to', themeName);
    } else {
        console.log('Theme unchanged');
    }
    
    // Создаем событие изменения темы для других скриптов
    const event = new CustomEvent('themeChanged', { detail: { theme: themeName } });
    document.dispatchEvent(event);
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
    // Проверяем, есть ли уже уведомление, и удаляем его
    const existingNotification = document.querySelector('.theme-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    // Создаем новое уведомление
    const notification = document.createElement('div');
    notification.className = 'theme-notification';
    notification.textContent = `Тема изменена на "${themeName}"`;
    
    // Добавляем уведомление на страницу
    document.body.appendChild(notification);
    
    // Анимация появления
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Удаляем уведомление через 3 секунды
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 500);
    }, 3000);
}

document.addEventListener('DOMContentLoaded', function() {
    // Определяем предпочтения пользователя по системным настройкам
    const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Проверяем сохраненную тему в localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        setTheme(savedTheme);
    } else if (prefersDarkMode) {
        // Если тема не сохранена, но система в темном режиме
        setTheme('dark-theme');
    }
    
    // Добавляем обработчики для пунктов меню в шапке
    const themeMenuItems = document.querySelectorAll('.dropdown-item[class*="theme-switcher-"]');
    
    themeMenuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const theme = e.currentTarget.getAttribute('data-theme');
            addTransitionClass();
            setTheme(theme);
        });
    });
    
    // Добавляем переключатель тем, если его еще нет
    if (!document.querySelector('.theme-switcher')) {
        const themeSwitcher = document.createElement('div');
        themeSwitcher.className = 'theme-switcher';
        
        // Кнопка светлой темы
        const lightBtn = document.createElement('button');
        lightBtn.className = 'theme-btn light-theme-btn';
        lightBtn.title = 'Светлая тема (Alt+1)';
        lightBtn.setAttribute('aria-label', 'Включить светлую тему');
        lightBtn.setAttribute('data-theme', '');
        lightBtn.innerHTML = '<i class="bi bi-brightness-high-fill"></i>';
        lightBtn.addEventListener('click', () => {
            addTransitionClass();
            setTheme('');
        });
        
        // Кнопка темной темы
        const darkBtn = document.createElement('button');
        darkBtn.className = 'theme-btn dark-theme-btn';
        darkBtn.title = 'Темная тема (Alt+2)';
        darkBtn.setAttribute('aria-label', 'Включить темную тему');
        darkBtn.setAttribute('data-theme', 'dark-theme');
        darkBtn.innerHTML = '<i class="bi bi-moon-fill"></i>';
        darkBtn.addEventListener('click', () => {
            addTransitionClass();
            setTheme('dark-theme');
        });
        
        // Кнопка Minecraft темы
        const minecraftBtn = document.createElement('button');
        minecraftBtn.className = 'theme-btn minecraft-theme-btn';
        minecraftBtn.title = 'Minecraft тема (Alt+3)';
        minecraftBtn.setAttribute('aria-label', 'Включить тему Minecraft');
        minecraftBtn.setAttribute('data-theme', 'minecraft-theme');
        minecraftBtn.innerHTML = '<i class="bi bi-grid-3x3-gap-fill"></i>';
        minecraftBtn.addEventListener('click', () => {
            addTransitionClass();
            setTheme('minecraft-theme');
        });
        
        // Добавляем кнопки в переключатель
        themeSwitcher.appendChild(lightBtn);
        themeSwitcher.appendChild(darkBtn);
        themeSwitcher.appendChild(minecraftBtn);
        
        // Добавляем переключатель на страницу
        document.body.appendChild(themeSwitcher);
        
        // Добавляем обработчик клавиатурных комбинаций для переключения тем
        document.addEventListener('keydown', function(event) {
            // Alt + 1 для светлой темы
            if (event.altKey && event.key === '1') {
                addTransitionClass();
                setTheme('');
                event.preventDefault();
            }
            // Alt + 2 для темной темы
            else if (event.altKey && event.key === '2') {
                addTransitionClass();
                setTheme('dark-theme');
                event.preventDefault();
            }
            // Alt + 3 для Minecraft темы
            else if (event.altKey && event.key === '3') {
                addTransitionClass();
                setTheme('minecraft-theme');
                event.preventDefault();
            }
        });
    }
    
    // Следим за изменениями системной темы
    if (window.matchMedia) {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
            if (!localStorage.getItem('theme')) {
                // Меняем тему только если пользователь не выбрал тему вручную
                if (event.matches) {
                    // Переключение на темную тему
                    addTransitionClass();
                    setTheme('dark-theme');
                } else {
                    // Переключение на светлую тему
                    addTransitionClass();
                    setTheme('');
                }
            }
        });
    }
    
    // Для отладки
    console.log('Theme system initialized. Current theme:', document.body.className || 'default (light)');
}); 