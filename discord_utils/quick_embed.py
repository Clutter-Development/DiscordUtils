# TODO: docs.
from typing import TYPE_CHECKING, Protocol, TypedDict, overload

import discord

if TYPE_CHECKING:
    import datetime

    from typing_extensions import Self

    class StyleDict(TypedDict):
        EMOJIS: dict[str, str]
        COLORS: dict[str, int]


class QuickEmbed(discord.Embed):
    def __init__(
        self,
        title: str | None = None,
        description: str | None = None,
        *,
        url: str | None = None,
        timestamp: datetime.datetime | None = None,
        color: int | discord.Color | None = None,
    ):
        super().__init__(
            title=title,
            description=description,
            url=url,
            timestamp=timestamp,
            color=color,
        )

    def add_field(self, title: str, description: str, *, inline: bool = False) -> Self:
        return super().add_field(name=title, value=description, inline=inline)


class PartialQuickEmbed(Protocol):
    def __call__(
        self,
        title: str | None = None,
        description: str | None = None,
        *,
        url: str | None = None,
        timestamp: datetime.datetime | None = None,
    ) -> QuickEmbed:
        ...


class QuickEmbedCreator:
    def __init__(self, style: StyleDict) -> None:
        self._style = style

    def __getattr__(self, item: str) -> PartialQuickEmbed:
        return self.__call__(item)

    @overload
    def __call__(self, asset_type: str, /) -> PartialQuickEmbed:
        ...

    @overload
    def __call__(
        self, asset_type: str, /, title: str | None = None, description: str | None = None, **kwargs
    ) -> QuickEmbed:
        ...

    def __call__(
        self,
        asset_type: str,
        /,
        title: str | None = None,
        description: str | None = None,
        **kwargs,
    ) -> QuickEmbed | PartialQuickEmbed:
        def inner(
            title: str | None = title,
            description: str | None = description,
            **kwargs_,
        ) -> QuickEmbed:
            nonlocal asset_type
            asset_type = asset_type.upper()

            if not kwargs_:
                kwargs_ = kwargs

            title_ = (
                f"{self._style.get('EMOJIS', {}).get(asset_type, '')} {title}".strip()
                if title
                else None
            )

            return QuickEmbed(
                title=title_,
                description=description,
                color=self._style.get("COLORS", {}).get(asset_type),
                **kwargs_,
            )

        if not any([title, description, kwargs]):
            return inner

        return inner()
