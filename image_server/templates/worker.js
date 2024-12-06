onmessage = function (e) {
    const url = e.data.url;

    async function fetchData() {
        //while (true) {
            try {
                const response = await fetch(url);
                const plotData = await response.json();
                postMessage(plotData); // Send the updated plot data to the main thread
            } catch (error) {
                console.error('Error fetching plot data:', error);
                postMessage(null); // Send null in case of an error
            }
            //await new Promise(resolve => setTimeout(resolve, 1000));
        //}
    }
};
