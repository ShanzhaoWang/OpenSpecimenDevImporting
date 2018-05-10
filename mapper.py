import logging


class Mapper(object):

    def __init__(self, df):
        self.df = df
        self.transforms = {}
        self.renames = {}
        self.rename_funcs = []
        self.columns_to_remove = []

    def rename_func(self, func):
        self.rename_funcs.append(func)
        return self

    def rename(self, old_column, new_column):
        self.renames.update({old_column: new_column})
        return self

    def drop_cols(self, cols):
        for col in cols:
            self.drop_col(col)
        return self

    def drop_col(self, col_name):
        assert col_name not in self.transforms.keys(), "Cannot apply transformation to a dropped column."
        self.columns_to_remove.append(col_name)
        return self

    def transform(self, col_name, func):
        if col_name in self.transforms.keys():
            self.transform[col_name].append(func)
        else:
            self.transforms.update({col_name: [func]})

        return self

    def apply(self):
        df = self.df

        logging.info("Renaming columns")

        for func in self.rename_funcs:
            df.rename(columns=func, inplace=True)

        logging.info("Renaming individual columns.")
        # Rename all the columns first...
        df.rename(columns=self.renames, inplace=True)

        logging.info("Dropping Columns")
        df.drop(columns=self.columns_to_remove)

        logging.info("Applying Functions")
        for col, funcs in self.transforms.items():
            logging.debug("Applying transforms for column: " + str(col))
            for func in funcs:
                df[col] = df[col].apply(func)

        return self

    def to_df(self):
        return self.df

    def save(self, filename):
        assert filename.endswith(".csv"), "File must end in .csv"
        logging.info("Saving output to file: " + str(filename))
        self.df.to_csv(filename)
