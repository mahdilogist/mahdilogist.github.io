const cityForm = document.querySelector('form');
const card = document.querySelector('.card');
const details = document.querySelector('.details');
const time = document.querySelector('img.time');
const icon = document.querySelector('.icon img')

// update UI
const updateUi = data => {

    // const cityDets = data.citydets;
    // const weather = data.weather;

    // destructure properties
    const {citydets, weather} = data;


// update details template
    details.innerHTML = `
    <h5 class="my-3">${citydets.EnglishName}</h5>
    <div class="my-3">${weather.WeatherText}</div>
    <div class="my-4 display-5">
        <span>${weather.Temperature.Metric.Value}</span>
        <span>&deg;c</span>
    </div>`;

    
    // update day-night and icon
    const iconSrc = `/icons/${weather.WeatherIcon}.svg`;
    icon.setAttribute('src', iconSrc);

    // let timeSrc = null;
    // if (weather.IsDayTime) {
    //     timeSrc = '/weather/icons/IMG-20181110-020814-797.jpg';
    // } else {
    //     timeSrc = '/weather/icons/night.jpg';
    // }

    let timeSrc = weather.IsDayTime ? '/icons/IMG-20181110-020814-797.jpg': '/icons/night.jpg';

    time.setAttribute('src', timeSrc);

    // remove display none if it present
    if (card.classList.contains('d-none')) {
        card.classList.remove('d-none');
    };


};

// update city
const updateCity = async(city) => {

    const citydets = await getCity(city);
    const weather = await getWeather(citydets.Key);

    return {
        citydets : citydets,
        weather : weather
    };
}

cityForm.addEventListener('submit', e => {
    e.preventDefault();

    // get city name
    const city = cityForm.city.value;
    cityForm.reset();

    // update ui with new city
    updateCity(city)
    .then(data => updateUi(data))
    .catch(err => console.log(err));
})