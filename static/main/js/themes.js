/**
 * Premium Theme System
 * Handles theme switching, persistence, and transitions.
 */

const THEMES = {
    LIGHT: '',
    DARK: 'dark-theme',
    MINECRAFT: 'minecraft-theme'
};

const THEME_NAMES = {
    [THEMES.LIGHT]: 'Светлая',
    [THEMES.DARK]: 'Темная',
    [THEMES.MINECRAFT]: 'Minecraft'
};

const THEME_COLORS = {
    [THEMES.LIGHT]: '#fcfcfd',
    [THEMES.DARK]: '#0f172a',
    [THEMES.MINECRAFT]: '#5c8d44'
};

/**
 * Applies the specified theme to the document body.
 * @param {string} themeName - The class name of the theme.
 * @param {boolean} isInitialLoad - Whether this is the first theme setup on page load.
 */
function setTheme(themeName, isInitialLoad = false) {
    const prevTheme = document.body.className.split(' ').filter(c => Object.values(THEMES).includes(c))[0] || THEMES.LIGHT;
    
    // Standardize theme name
    if (themeName === 'light-theme') themeName = THEMES.LIGHT;
    
    // Remove all existing theme classes
    Object.values(THEMES).forEach(t => {
        if (t) document.body.classList.remove(t);
    });
    
    // Add new theme class if not light
    if (themeName) {
        document.body.classList.add(themeName);
    }
    
    localStorage.setItem('theme', themeName);
    
    // Update theme toggle buttons / dropdown items
    updateUIStates(themeName);
    
    // Update browser theme color
    updateMetaThemeColor(THEME_COLORS[themeName] || THEME_COLORS[THEMES.LIGHT]);
    
    // Check if session has been initialized to avoid notifications on every load
    const sessionInitialized = sessionStorage.getItem('themeInitialized');
    
    // Show notification if theme actually changed AND it's not the initial load AND session was already ready
    if (!isInitialLoad && prevTheme !== themeName && sessionInitialized) {
        showThemeNotification(THEME_NAMES[themeName] || 'Стандартная');
        
        // Dispatch event for other listeners
        const event = new CustomEvent('themeChanged', { 
            detail: { theme: themeName, prevTheme } 
        });
        document.dispatchEvent(event);
    }
    
    // Mark session as initialized after the first setTheme call
    sessionStorage.setItem('themeInitialized', 'true');
}

/**
 * Updates active states for theme switchers in the UI.
 */
function updateUIStates(activeTheme) {
    // Standardize for comparison
    const target = activeTheme === THEMES.LIGHT ? '' : activeTheme;

    // Update dropdown items
    const menuItems = document.querySelectorAll('.dropdown-item[class*="theme-switcher-"]');
    menuItems.forEach(item => {
        const itemTheme = item.getAttribute('data-theme') === 'light-theme' ? '' : item.getAttribute('data-theme');
        if (itemTheme === target) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });

    // Update floating buttons if they exist
    const floatingButtons = document.querySelectorAll('.theme-btn');
    floatingButtons.forEach(btn => {
        const btnTheme = btn.getAttribute('data-theme') === 'light-theme' ? '' : btn.getAttribute('data-theme');
        if (btnTheme === target) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

/**
 * Updates the meta theme-color tag for mobile browsers.
 */
function updateMetaThemeColor(color) {
    let metaThemeColor = document.querySelector('meta[name="theme-color"]');
    if (!metaThemeColor) {
        metaThemeColor = document.createElement('meta');
        metaThemeColor.name = 'theme-color';
        document.head.appendChild(metaThemeColor);
    }
    metaThemeColor.content = color;
}

/**
 * Displays a premium notification briefly.
 */
function showThemeNotification(themeNameRU) {
    let notification = document.querySelector('.theme-notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.className = 'theme-notification';
        document.body.appendChild(notification);
    }
    
    notification.innerHTML = `<i class="bi bi-palette-fill me-2"></i> Тема: <strong>${themeNameRU}</strong>`;
    
    // Trigger show
    setTimeout(() => notification.classList.add('show'), 10);
    
    // Auto-hide
    if (window.themeNotificationTimeout) clearTimeout(window.themeNotificationTimeout);
    window.themeNotificationTimeout = setTimeout(() => {
        notification.classList.remove('show');
    }, 2500);
}

/**
 * Wraps theme setting with a transition class for smoothness.
 */
function switchThemeWithTransition(themeName) {
    document.body.classList.add('theme-transition');
    setTheme(themeName); // isInitialLoad defaults to false
    setTimeout(() => {
        document.body.classList.remove('theme-transition');
    }, 600);
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    // Check saved preference or system default
    const savedTheme = localStorage.getItem('theme');
    const systemPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme !== null) {
        setTheme(savedTheme, true); // true = Initial load
    } else if (systemPrefersDark) {
        setTheme(THEMES.DARK, true);
    } else {
        setTheme(THEMES.LIGHT, true);
    }
    
    // Bind click events to all switchers
    const switchers = document.querySelectorAll('[class*="theme-switcher-"], .theme-btn');
    switchers.forEach(el => {
        el.addEventListener('click', (e) => {
            e.preventDefault();
            const theme = el.getAttribute('data-theme');
            switchThemeWithTransition(theme);
        });
    });
    
    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            switchThemeWithTransition(e.matches ? THEMES.DARK : THEMES.LIGHT);
        }
    });

    // Keyboard Shortcuts (Alt + 1/2/3)
    document.addEventListener('keydown', (e) => {
        if (e.altKey && e.key === '1') switchThemeWithTransition(THEMES.LIGHT);
        if (e.altKey && e.key === '2') switchThemeWithTransition(THEMES.DARK);
        if (e.altKey && e.key === '3') switchThemeWithTransition(THEMES.MINECRAFT);
    });
});