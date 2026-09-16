import Feature04Domain

public enum Feature04DataRepository {
    public static func load(_ id: Int) -> Feature04DomainModel {
        Feature04DomainModel(id: id, title: "Feature 4")
    }
}
