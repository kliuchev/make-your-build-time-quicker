import Feature23Domain

public enum Feature23DataRepository {
    public static func load(_ id: Int) -> Feature23DomainModel {
        Feature23DomainModel(id: id, title: "Feature 23")
    }
}
