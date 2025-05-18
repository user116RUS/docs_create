<script>
document.addEventListener('DOMContentLoaded', function() {
    // Получаем форму и кнопку отправки
    const form = document.querySelector('form');
    const submitButton = document.getElementById('submitButton');
    
    // Инициализируем выпадающий список предложений для поля "Название услуги"
    function initServiceNameSuggestions() {
        // Список предложений для названия услуги
        const serviceSuggestions = [
            'Квест по ПДД "Безопасные дороги"',
            'Квест "Команда первых"',
            'Квест "Джуманджи"',
            'Квест "Школьный спасатель"',
            'Мастер-класс по инженерии',
            'Электронный квест "Звездные войны"',
            'Мастер-класс по робототехнике'
        ];
        
        // Получаем элементы для работы с предложениями
        const serviceNameInput = document.getElementById('serviceName');
        const suggestionsContainer = document.getElementById('serviceNameSuggestions');
        
        if (serviceNameInput && suggestionsContainer) {
            // Очищаем выпадающий список
            suggestionsContainer.innerHTML = '';
            
            // Заполняем выпадающий список предложениями
            serviceSuggestions.forEach(suggestion => {
                const suggestionItem = document.createElement('div');
                suggestionItem.className = 'suggestion-item';
                suggestionItem.textContent = suggestion;
                suggestionItem.addEventListener('click', () => {
                    serviceNameInput.value = suggestion;
                    suggestionsContainer.classList.remove('show');
                    
                    // Воспроизводим звук при выборе в теме Minecraft
                    if (document.body.classList.contains('minecraft-theme')) {
                        playMinecraftSound('click');
                    }
                });
                suggestionsContainer.appendChild(suggestionItem);
            });
            
            // Показываем выпадающий список при фокусе на поле ввода
            serviceNameInput.addEventListener('focus', () => {
                suggestionsContainer.classList.add('show');
                
                // Воспроизводим звук при фокусе в теме Minecraft
                if (document.body.classList.contains('minecraft-theme')) {
                    playMinecraftSound('click');
                }
            });
            
            // Фильтруем предложения при вводе текста
            serviceNameInput.addEventListener('input', () => {
                const inputValue = serviceNameInput.value.toLowerCase();
                const suggestionItems = suggestionsContainer.querySelectorAll('.suggestion-item');
                
                let hasVisibleItems = false;
                
                suggestionItems.forEach(item => {
                    const suggestionText = item.textContent.toLowerCase();
                    if (suggestionText.includes(inputValue)) {
                        item.style.display = 'block';
                        hasVisibleItems = true;
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                // Показываем или скрываем выпадающий список в зависимости от наличия совпадений
                if (hasVisibleItems) {
                    suggestionsContainer.classList.add('show');
                } else {
                    suggestionsContainer.classList.remove('show');
                }
            });
            
            // Скрываем выпадающий список при клике вне поля ввода и списка
            document.addEventListener('click', (event) => {
                if (!event.target.closest('.suggestions-container')) {
                    suggestionsContainer.classList.remove('show');
                }
            });
        }
    }
    
    // Функция для воспроизведения звуков Minecraft
    function playMinecraftSound(type) {
        // Звуки Minecraft (можно заменить на реальные звуки из игры)
        const sounds = {
            click: 'https://www.myinstants.com/media/sounds/minecraft-click.mp3',
            success: 'https://www.myinstants.com/media/sounds/minecraft_xp.mp3'
        };
        
        if (sounds[type]) {
            const audio = new Audio(sounds[type]);
            audio.volume = 0.5;
            audio.play();
        }
    }
    
    // Функции для модального окна услуг
    const serviceModalElement = document.getElementById('serviceModal');
    const deleteServiceModalElement = document.getElementById('deleteServiceModal');
    
    // Проверяем, что элементы существуют и bootstrap доступен
    let serviceModal, deleteServiceModal;
    if (typeof bootstrap !== 'undefined') {
        if (serviceModalElement) {
            serviceModal = new bootstrap.Modal(serviceModalElement);
        }
        if (deleteServiceModalElement) {
            deleteServiceModal = new bootstrap.Modal(deleteServiceModalElement);
        }
    } else {
        console.error('Bootstrap не найден! Убедитесь, что библиотека правильно подключена.');
    }
    
    const serviceForm = document.getElementById('serviceForm');
    const serviceIdField = document.getElementById('serviceId');
    const serviceNameField = document.getElementById('serviceName');
    const serviceDateField = document.getElementById('serviceDate');
    const categoriesContainer = document.getElementById('categoriesContainer');
    const addCategoryBtn = document.getElementById('addCategoryBtn');
    const saveServiceBtn = document.getElementById('saveServiceBtn');
    const deleteServiceName = document.getElementById('deleteServiceName');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    
    // Добавляем обработчик на кнопку "Добавить новую услугу"
    const createServiceBtn = document.getElementById('createServiceBtn');
    if (createServiceBtn) {
        createServiceBtn.addEventListener('click', function(e) {
            e.preventDefault();
            openServiceModal();
        });
    }
    
    // Обработчик на кнопки редактирования услуг
    document.addEventListener('click', function(e) {
        if (e.target.closest('.edit-service-btn')) {
            e.preventDefault();
            const serviceCard = e.target.closest('.service-card');
            const serviceId = serviceCard.dataset.serviceId;
            openServiceModal(serviceId);
        }
    });
    
    // Обработчик на кнопки удаления услуг
    document.addEventListener('click', function(e) {
        if (e.target.closest('.delete-service-btn')) {
            e.preventDefault();
            const serviceCard = e.target.closest('.service-card');
            const serviceId = serviceCard.dataset.serviceId;
            const serviceName = serviceCard.querySelector('.form-check-label').textContent.trim();
            openDeleteModal(serviceId, serviceName);
        }
    });
    
    // Функция открытия модального окна услуги
    function openServiceModal(serviceId = null) {
        // Проверяем, инициализировано ли модальное окно
        if (!serviceModal) {
            alert('Не удалось открыть модальное окно. Проблема с Bootstrap.');
            return;
        }
        
        // Очищаем форму
        serviceForm.reset();
        serviceIdField.value = '';
        categoriesContainer.innerHTML = '';
        
        if (serviceId) {
            // Редактирование существующей услуги
            const serviceCard = document.querySelector(`.service-card[data-service-id="${serviceId}"]`);
            if (serviceCard) {
                // Заполняем поля формы
                serviceIdField.value = serviceId;
                const nameLabel = serviceCard.querySelector('.form-check-label').textContent.trim();
                const nameParts = nameLabel.split('(');
                serviceNameField.value = nameParts[0].trim();
                serviceDateField.value = nameParts[1].replace(')', '').trim();
                
                // Добавляем категории
                const categoryItems = serviceCard.querySelectorAll('.category-item');
                categoryItems.forEach(function(item) {
                    const viewersText = item.querySelector('div:first-child').textContent.trim();
                    const priceText = item.querySelector('div:last-child').textContent.trim();
                    
                    const viewers = parseInt(viewersText.replace(' чел.', ''));
                    const price = parseFloat(priceText.replace(' руб.', ''));
                    
                    addCategoryRow(viewers, price);
                });
                
                // Меняем заголовок
                document.getElementById('serviceModalLabel').textContent = 'Редактирование услуги';
            }
        } else {
            // Создание новой услуги
            document.getElementById('serviceModalLabel').textContent = 'Создание новой услуги';
            // Добавляем пустую категорию
            addCategoryRow();
        }
        
        // Открываем модальное окно
        serviceModal.show();
        
        // Инициализируем выпадающий список предложений
        initServiceNameSuggestions();
    }
    
    // Функция открытия модального окна подтверждения удаления
    function openDeleteModal(serviceId, serviceName) {
        // Проверяем, инициализировано ли модальное окно
        if (!deleteServiceModal) {
            alert('Не удалось открыть модальное окно. Проблема с Bootstrap.');
            return;
        }
        
        document.getElementById('deleteServiceName').textContent = serviceName;
        confirmDeleteBtn.dataset.serviceId = serviceId;
        deleteServiceModal.show();
    }
    
    // Функция для инициализации обработчиков событий карточки
    function initServiceCard(card) {
        // Добавляем обработчик клика на карточку
        card.addEventListener('click', function(e) {
            // Проверяем, что клик не был на кнопке редактирования или чекбоксе
            if (!e.target.closest('a') && !e.target.closest('.form-check-input') && !e.target.closest('button')) {
                const checkbox = this.querySelector('.service-checkbox');
                if (checkbox) {
                    checkbox.checked = !checkbox.checked;
                    
                    // Имитируем событие change на чекбоксе
                    const event = new Event('change');
                    checkbox.dispatchEvent(event);
                }
            }
        });
        
        // Добавляем обработчик на чекбокс
        const checkbox = card.querySelector('.service-checkbox');
        if (checkbox) {
            checkbox.addEventListener('change', function() {
                updateServicesField();
                updateServiceCardSelection(this);
                updateServicesSummary();
            });
        }
        
        // Добавляем обработчик на кнопку редактирования
        const editBtn = card.querySelector('.edit-service-btn');
        if (editBtn) {
            editBtn.addEventListener('click', function(e) {
                e.preventDefault();
                const serviceId = card.dataset.serviceId;
                openServiceModal(serviceId);
            });
        }
        
        // Добавляем обработчик на кнопку удаления
        const deleteBtn = card.querySelector('.delete-service-btn');
        if (deleteBtn) {
            deleteBtn.addEventListener('click', function(e) {
                e.preventDefault();
                const serviceId = card.dataset.serviceId;
                const serviceName = card.querySelector('.form-check-label').textContent.trim();
                openDeleteModal(serviceId, serviceName);
            });
        }
    }
    
    // Остальной код JavaScript (инициализация календаря, обработка файлов, и т.д.)
    // ...
});
</script>
{% endblock %} 
