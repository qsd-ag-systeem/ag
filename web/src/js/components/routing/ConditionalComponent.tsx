import React from "react";
import { Navigate } from "react-router-dom";
import ErrorBoundary from "../ErrorBoundary";
import { useDocumentTitle } from "@mantine/hooks";
import { APP_NAME } from "../../constants";

type Props = {
  condition: boolean;
  Component: React.ComponentType;
  redirectTo?: string;
  title?: string;
};

export const ConditionalComponent = (props: Props) => {
  const { condition, Component, redirectTo, title = "" } = props;
  useDocumentTitle(`${title === "" ? "" : `${title} - `} ${APP_NAME}`);

  if (!condition) return <Navigate to={redirectTo ?? "/login"} />;

  return (
    <ErrorBoundary>
      <Component />
    </ErrorBoundary>
  );
};
