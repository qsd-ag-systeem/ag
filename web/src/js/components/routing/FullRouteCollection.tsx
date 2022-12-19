import { Route, Routes } from "react-router-dom";
import Home from "../../pages/Home";
import Enroll from "../../pages/Enroll";
import NotFound from "../../pages/NotFound";
import { ConditionalComponent } from "./ConditionalComponent";

export default function FullRouteCollection() {
  // TODO: Auth
  const isAuthed = true;

  return (
    <Routes>
      <Route
        path={"/"}
        element={<ConditionalComponent condition={isAuthed} Component={Home} title={"Home"} />}
      />

      <Route
        path={"/enroll"}
        element={<ConditionalComponent condition={isAuthed} Component={Enroll} title={"Enroll"} />}
      />

      <Route
        path={"*"}
        element={<ConditionalComponent condition={isAuthed} Component={NotFound} title={"404"} />}
      />
    </Routes>
  );
}
