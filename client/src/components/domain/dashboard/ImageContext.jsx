import { createContext, useState, useContext } from "react";

const ImageContext = createContext();

export const ImageProvider = ({ children }) => {
    const [image, setImage] = useState(null);

    return (
        <ImageContext.Provider value={{ image, setImage }}>
            {children}
        </ImageContext.Provider>
    );
};

export const useImage = () => useContext(ImageContext);