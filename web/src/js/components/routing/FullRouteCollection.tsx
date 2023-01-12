import { Route, Routes } from "react-router-dom";
import CrossSearch from "../../pages/cross-search";
import Search from "../../pages/search";
import NotFound from "../../pages/NotFound";
import { ConditionalComponent } from "./ConditionalComponent";

export default function FullRouteCollection() {
  // TODO: Auth
  const isAuthed = true;

  return (
    <Routes>
      <Route
        path={"/"}
        element={<ConditionalComponent condition={isAuthed} Component={Search} title={"Home"} />}
      />

      <Route
        path={"/cross-search"}
        element={
          <ConditionalComponent
            condition={isAuthed}
            Component={CrossSearch}
            title={"Kruiszoeken"}
          />
        }
      />

      <Route
        path={"*"}
        element={<ConditionalComponent condition={isAuthed} Component={NotFound} title={"404"} />}
      />
    </Routes>
  );
}
