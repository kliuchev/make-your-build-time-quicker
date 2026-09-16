import Feature05Domain

public enum Feature05DataRepository {
    public static func load(_ id: Int) -> Feature05DomainModel {
        Feature05DomainModel(id: id, title: "Feature 5")
    }
}
