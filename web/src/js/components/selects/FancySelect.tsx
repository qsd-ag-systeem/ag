import { Autocomplete, AutocompleteItem, AutocompleteStylesNames, Loader } from "@mantine/core";
import { DefaultProps } from "@mantine/styles";
import React, { ReactNode, useRef, useState } from "react";
import { DEBOUNCE_TIMEOUT } from "../../constants";

type FancySelectProps<T> = DefaultProps<AutocompleteStylesNames> & {
  error?: React.ReactNode;
  defaultValue?: string;
  onItemSubmit: (value: AutocompleteItem) => void;
  onClear: () => void;
  required?: boolean;
  label?: string;
  placeholder?: string;
  queryFn: (query: string) => any;
  labelRenderer: (value: T) => ReactNode;
};

export function FancySelect<T extends { id?: number | string }>(props: FancySelectProps<T>) {
  const { onClear, defaultValue, queryFn, labelRenderer, ...restProps } = props;
  const timeoutRef = useRef<number>(-1);
  const [value, setValue] = useState(defaultValue);
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<AutocompleteItem[]>([]);

  const onChange = (val: string = "") => {
    // Reset the wait period before sending the request to prevent spamming the API.
    window.clearTimeout(timeoutRef.current);

    setValue(val);
    setData([]);
    onClear();

    if (val.trim().length === 0) {
      setLoading(false);
    } else {
      setLoading(true);

      // Send the request after waiting the global DEBOUNCE_TIMEOUT to ensure that the typing has stopped.
      timeoutRef.current = window.setTimeout(async () => {
        let filteredData = await queryFn(val);
        setLoading(false);

        setData(
          filteredData.data.map((value: T) => {
            return {
              value: `${labelRenderer(value)}`,
              data: value,
            };
          })
        );
      }, DEBOUNCE_TIMEOUT);
    }
  };

  return (
    <Autocomplete
      {...restProps}
      data={data}
      value={value}
      limit={20}
      onChange={onChange}
      styles={{ rightSection: { pointerEvents: "none" } }}
      rightSection={loading && <Loader size={16} />}
    />
  );
}
