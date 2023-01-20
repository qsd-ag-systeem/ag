import { createContext, ReactNode, useState } from "react";

type Props = {
  children?: ReactNode;
};

type FacialBorderContextProps = {
  facialBorderVisible: boolean;
  setFacialBorderVisible: (value: boolean) => void;
};

export const FacialBorderContext = createContext<FacialBorderContextProps>({
  facialBorderVisible: true,
  setFacialBorderVisible: () => {},
});

export default function FacialBorderProvider(props: Props) {
  const [facialBorderVisible, setFacialBorderVisible] = useState(true);

  return (
    <FacialBorderContext.Provider value={{ facialBorderVisible, setFacialBorderVisible }}>
      {props.children}
    </FacialBorderContext.Provider>
  );
}
