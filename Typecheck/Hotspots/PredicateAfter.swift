enum Status { case active, paused }

struct Model {
    var primary: Status
    var secondary: Status?
    var fallback: Status
}

func matches<Field, Item>(
    _ item: Item, key: KeyPath<Item, Field>,
    where predicate: (Item) -> Bool
) -> Bool { predicate(item) }

func value(_ model: Model) -> Bool {
    matches(model, key: \.primary) { (item: Model) -> Bool in
        item.primary == .active &&
        item.secondary == .active &&
        item.fallback == .active
    }
}
