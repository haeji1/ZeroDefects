import React from "react";
import { ClipLoader, MoonLoader } from "react-spinners";

const override = {
  display: "flex",
  margin: "0 auto",
  borderColor: "#E50915",
  textAlign: "center",
};

const Loading = ({ loading }) => {
  return (
    <div>
        <h3>잠시만 기다려 주세요.</h3>
      <MoonLoader
        color="#1428A0"
        loading={loading}
        cssOverride={override}
        size={150}
      />
    </div>
  );
};

export default Loading;