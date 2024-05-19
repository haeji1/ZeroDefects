import React from "react";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import "chartjs-plugin-zoom";

const ChartComponent = ({ start_index, title, data_set }) => {
  // create data
  const data = {
    labels: Array.from({ length: data_set.length }, (_, i) => start_index + i),
    datasets: [
      {
        label: title,
        data: data_set,
        borderColor: "blue",
        borderWidth: 0.5,
        pointRadius: 0,
      },
    ],
  };

  const options = {
    scales: {
      x: {
        type: "linear",
      },
      y: {
        beginAtZero: true,
        max: Math.ceil(Math.max(...data_set) * 1.2),
      },
    },

    animation: false,
    responsive: true,
    maintainAspectRatio: false,

    plugins: {
      tooltip: {
        enable: false,
      },
      decimation: {
        enabled: true,
        algorithm: "min-max", // 또는 'min-max'
      },

      // chartjs plugins zoom
      zoom: {
        limits: {
          x: { min: "original", max: "original" },
        },

        zoom: {
          wheel: {
            enabled: true,
          },
          pinch: {
            enabled: true,
            mode: "x",
          },
          mode: "xy",
          rangeMin: {
            x: null,
          },
          rangeMax: {
            x: data_set.length,
          },
        },
        pan: {
          enabled: true,
          mode: "xy",
          rangeMin: {
            x: null,
          },
          rangeMax: {
            x: data_set.length,
          },
        },
      },
    },

    interaction: {
      mode: "index",
      intersect: false,
    },
    hover: {
      mode: null,
    },

    elements: {
      line: {
        tension: 0, // 곡선을 직선으로 변경
      },
      point: {
        radius: 0, // 데이터 포인트를 숨깁니다.
      },
    },
  };

  return (
    <div>
      <Line data={data} options={options} height={400} />
    </div>
  );
};

export default ChartComponent;
